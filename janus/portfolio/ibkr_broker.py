"""janus.portfolio.ibkr_broker — IBKR implementation of ``PaperBroker.execute``.

Not a Janus module. It is the live-broker extension point documented in
``janus/execution.py``.

Semantics:

- ``FLAT``  -> flatten (long or short); return ``None``.
- ``LONG``  -> buy ``position_size * equity / price`` shares; return ``Fill``.
- ``SHORT`` -> buy inverse-ETF proxy in ``SHORT_PROXIES``; log and return
               ``None`` if no proxy.

Session maintenance
-------------------
The IBKR Client Portal Gateway requires:

- A ``POST /tickle`` every ~60 seconds. Without it the gateway drops the
  session at ~5 minutes and every subsequent request returns 401.
- Manual browser re-authentication every 24 hours. The SSO token expires
  hard at 24 hours; nothing programmatic can extend it. Only the operator,
  opening ``https://localhost:5000`` and logging in, resets the clock.

This module handles both as far as they can be automated:

- ``tickle()`` sends ``POST /tickle``.
- ``check_session()`` sends ``POST /iserver/auth/status`` and caches the
  result.
- ``_maybe_maintain_session()`` is called at the start of every ``_request``
  and performs the above on interval. A 401/403 on a real request triggers
  one re-check plus one retry; if the session is still unauthenticated, an
  ``IBKRAuthError`` is raised.
- ``IBKRBroker.execute`` catches ``IBKRAuthError``, logs at CRITICAL, and
  re-raises. A dead session is not a transient error; it must be loud.

The 24-hour re-auth cannot be automated. When the SSO token expires,
``IBKRAuthError`` propagates and the operator must open
``https://localhost:5000``, log in, and restart the trading loop.

Known limitations
-----------------
- ``self.equity`` captured at construction. Set ``broker.equity`` before
  ``execute`` if it has changed.
- ``Fill.action`` uses ``intent.action.value``. Verify against
  ``janus/execution.py`` before deployment.
- On ``SHORT``, ``Fill`` records the intent symbol, not the proxy.
- Session maintenance only runs when requests are made. A pipeline that
  goes fully idle for more than ~5 minutes will lose the gateway session
  regardless of the intervals here; restart the loop or run a background
  tickle thread.

Requires ``requests``. Install from ``requirements.txt`` or
``pip install "requests>=2.32"``.
"""

from __future__ import annotations

import logging
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Final, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from janus.contracts import Action, TradeIntent
from janus.execution import Fill

logger = logging.getLogger("janus.portfolio.ibkr")

SHORT_PROXIES: Final[dict[str, str]] = {
    "SPY": "SH",
    "QQQ": "PSQ",
    "IWM": "RWM",
    "GDX": "DUST",
    "GDXJ": "JDST",
    "EWZ": "BZQ",
}

_FILL_HISTORY_LIMIT: Final[int] = 1000

_DEFAULT_TICKLE_INTERVAL: Final[float] = 60.0
_DEFAULT_AUTH_CHECK_INTERVAL: Final[float] = 300.0

# Endpoints that must not trigger session maintenance, either because they
# ARE the maintenance themselves or because they are the pre-auth probes.
_MAINTENANCE_PATHS: Final[frozenset[str]] = frozenset(
    {
        "/tickle",
        "/iserver/auth/status",
        "/iserver/reauthenticate",
        "/iserver/accounts",
        "/logout",
        "/sso/validate",
    }
)


class IBKRAuthError(RuntimeError):
    """Raised when the Client Portal Gateway session is not authenticated.

    The Client Portal Gateway requires manual browser re-authentication
    every 24 hours. When the SSO token expires, no programmatic call can
    extend it. The operator must:

    1. Open https://localhost:5000 in a browser.
    2. Log in with their IBKR credentials.
    3. Restart the trading loop.

    Until then, every request to an authenticated endpoint returns 401.
    This exception makes that failure loud instead of silent.
    """


class IBKRClient:
    """Minimal HTTP client for the IBKR Client Portal Web API.

    The client assumes the Client Portal Gateway is running at
    ``https://localhost:5000`` and the user has authenticated in a browser.
    Every request goes through the gateway; the gateway proxies to IBKR.

    Session maintenance is performed automatically on the first request
    and on interval thereafter. See the module docstring for details.
    """

    def __init__(
        self,
        account_id: str,
        gateway: str = "https://localhost:5000",
        verify_ssl: bool = False,
        timeout: int = 30,
        state_dir: str | Path = "./state",
        maintain_session: bool = True,
        tickle_interval: float = _DEFAULT_TICKLE_INTERVAL,
        auth_check_interval: float = _DEFAULT_AUTH_CHECK_INTERVAL,
    ) -> None:
        self.account_id = account_id
        self.base = f"{gateway.rstrip('/')}/v1/api"
        self.verify = verify_ssl
        self.timeout = timeout
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self._conid_cache_path = self.state_dir / "conid_cache.json"
        self._conid_cache: dict[str, int] = self._load_cache()

        self._maintain_session: bool = maintain_session
        self._tickle_interval: float = tickle_interval
        self._auth_check_interval: float = auth_check_interval
        self._last_tickle: float = 0.0
        self._last_auth_check: float = 0.0
        self._authenticated: bool = False

        self.session = requests.Session()
        self.session.mount(
            "https://",
            HTTPAdapter(
                max_retries=Retry(
                    total=3,
                    backoff_factor=1.0,
                    status_forcelist=[429, 500, 502, 503, 504],
                    allowed_methods=["GET", "POST", "DELETE"],
                )
            ),
        )

    # ─── cache ──────────────────────────────────────────────────────────

    def _load_cache(self) -> dict[str, int]:
        if not self._conid_cache_path.exists():
            return {}
        try:
            import json

            return json.loads(
                self._conid_cache_path.read_text(encoding="utf-8")
            )
        except Exception:
            return {}

    def _save_cache(self) -> None:
        import json

        self._conid_cache_path.write_text(
            json.dumps(self._conid_cache, indent=2), encoding="utf-8"
        )

    # ─── session maintenance ────────────────────────────────────────────

    def tickle(self) -> dict:
        """POST /tickle to refresh the gateway's session timer.

        Raises ``IBKRAuthError`` if the gateway reports 401/403.
        Returns the response body on success.
        """
        return self._request(
            "POST", "/tickle", _skip_maintenance=True
        )

    def check_session(self) -> bool:
        """POST /iserver/auth/status and cache the result.

        Returns ``True`` iff ``authenticated`` and ``connected`` are both
        true in the response body. Raises on network failure or on
        401/403 from the status endpoint itself.
        """
        try:
            body = self._request(
                "POST", "/iserver/auth/status", _skip_maintenance=True
            )
        except RuntimeError:
            self._authenticated = False
            raise
        self._authenticated = bool(body.get("authenticated")) and bool(
            body.get("connected")
        )
        self._last_auth_check = time.time()
        return self._authenticated

    def reauthenticate(self) -> dict:
        """POST /iserver/reauthenticate.

        Attempts to refresh the session without a browser round-trip. This
        works only while the SSO token is still valid (i.e. within 24 hours
        of the last browser login). After the SSO token expires, this call
        fails and only a browser re-authentication can restore the session.

        Callers should prefer this method over forcing a ``check_session``
        when they suspect the session is stale but not expired.
        """
        return self._request(
            "POST", "/iserver/reauthenticate", _skip_maintenance=True
        )

    def logout(self) -> dict:
        """POST /logout to terminate the gateway session."""
        self._authenticated = False
        return self._request(
            "POST", "/logout", _skip_maintenance=True
        )

    def session_status(self) -> dict:
        """Return a diagnostic dict describing the cached session state.

        Does not perform any network I/O. Useful for logging.
        """
        now = time.time()
        return {
            "authenticated": self._authenticated,
            "last_tickle_age_s": (
                now - self._last_tickle if self._last_tickle else None
            ),
            "last_auth_check_age_s": (
                now - self._last_auth_check if self._last_auth_check else None
            ),
            "tickle_interval_s": self._tickle_interval,
            "auth_check_interval_s": self._auth_check_interval,
            "maintain_session": self._maintain_session,
        }

    def _maybe_maintain_session(self) -> None:
        """Tickle and check auth if their intervals have elapsed.

        On the first request in a process, both intervals have elapsed
        (``_last_tickle`` and ``_last_auth_check`` start at 0.0), so the
        first request performs both.

        A tickle failure raises ``IBKRAuthError`` (fatal) or logs a
        warning (transient network failure). An auth-check failure raises
        ``IBKRAuthError``.
        """
        if not self._maintain_session:
            return

        now = time.time()

        if now - self._last_tickle >= self._tickle_interval:
            try:
                self.tickle()
                self._last_tickle = now
            except IBKRAuthError:
                self._authenticated = False
                raise
            except RuntimeError as exc:
                logger.warning(
                    "IBKR tickle failed (transient): %s", exc
                )

        if now - self._last_auth_check >= self._auth_check_interval:
            if not self.check_session():
                raise IBKRAuthError(
                    "IBKR session is not authenticated. "
                    "Open https://localhost:5000 in a browser and log in. "
                    "The Client Portal Gateway requires manual "
                    "re-authentication every 24 hours."
                )

    # ─── transport ──────────────────────────────────────────────────────

    def _request(
        self,
        method: str,
        path: str,
        params=None,
        body=None,
        _skip_maintenance: bool = False,
    ):
        if not _skip_maintenance and path not in _MAINTENANCE_PATHS:
            self._maybe_maintain_session()

        url = f"{self.base}{path}"
        try:
            response = self.session.request(
                method,
                url,
                params=params,
                json=body,
                timeout=self.timeout,
                verify=self.verify,
                headers={"Content-Type": "application/json"},
            )
        except requests.RequestException as exc:
            raise RuntimeError(f"IBKR network error: {exc}") from exc

        if response.status_code in (401, 403):
            # Session may have expired silently between the last tickle
            # and this request. Re-check once; retry once.
            if not _skip_maintenance:
                if self.check_session():
                    return self._request(
                        method,
                        path,
                        params=params,
                        body=body,
                        _skip_maintenance=True,
                    )
            raise IBKRAuthError(
                f"IBKR {response.status_code} on {method} {path}: "
                f"session is not authenticated. "
                f"Open https://localhost:5000 in a browser and log in. "
                f"The Client Portal Gateway requires manual "
                f"re-authentication every 24 hours."
            )

        if response.status_code >= 400:
            raise RuntimeError(
                f"IBKR {response.status_code}: {response.text[:200]}"
            )
        if response.status_code == 204:
            return {}
        try:
            return response.json()
        except ValueError:
            return {}

    # ─── reference data ─────────────────────────────────────────────────

    def resolve_conid(
        self, symbol: str, sec_type: str = "STK", exchange: str = "SMART"
    ) -> Optional[int]:
        key = f"{symbol}|{sec_type}|{exchange}"
        if key in self._conid_cache:
            return self._conid_cache[key]

        hits = self._request(
            "GET",
            "/iserver/secdef/search",
            params={"symbol": symbol, "secType": sec_type, "exchange": exchange},
        )
        if isinstance(hits, dict):
            hits = [hits]
        for hit in hits or []:
            conid = hit.get("conid")
            if conid:
                self._conid_cache[key] = int(conid)
                self._save_cache()
                return int(conid)
        return None

    # ─── orders ─────────────────────────────────────────────────────────

    def place_order(
        self,
        conid: int,
        side: str,
        quantity: float,
        order_type: str = "MKT",
        limit_price: Optional[float] = None,
    ) -> dict:
        order = {
            "conid": conid,
            "side": side.upper(),
            "orderType": order_type,
            "quantity": quantity,
            "tif": "DAY",
            "outsideRTH": False,
        }
        if order_type == "LMT":
            if limit_price is None:
                raise ValueError("limit_price is required for LMT orders")
            order["price"] = limit_price

        response = self._request(
            "POST",
            f"/iserver/account/{self.account_id}/orders",
            body={"orders": [order]},
        )
        for _ in range(3):
            if (
                isinstance(response, list)
                and response
                and "id" in response[0]
            ):
                response = self._request(
                    "POST",
                    f"/iserver/reply/{response[0]['id']}",
                    body={"confirmed": True},
                )
            else:
                break
        return response if isinstance(response, dict) else {"response": response}

    def buy(
        self,
        symbol: str,
        quantity: float,
        limit_price: Optional[float] = None,
        sec_type: str = "STK",
        exchange: str = "SMART",
    ) -> dict:
        conid = self.resolve_conid(symbol, sec_type, exchange)
        if conid is None:
            raise RuntimeError(f"could not resolve conid for {symbol}")
        order_type = "LMT" if limit_price is not None else "MKT"
        return self.place_order(conid, "BUY", quantity, order_type, limit_price)

    def sell(
        self,
        symbol: str,
        quantity: float,
        limit_price: Optional[float] = None,
        sec_type: str = "STK",
        exchange: str = "SMART",
    ) -> dict:
        conid = self.resolve_conid(symbol, sec_type, exchange)
        if conid is None:
            raise RuntimeError(f"could not resolve conid for {symbol}")
        order_type = "LMT" if limit_price is not None else "MKT"
        return self.place_order(
            conid, "SELL", quantity, order_type, limit_price
        )

    # ─── positions ──────────────────────────────────────────────────────

    def positions(self) -> dict[str, dict]:
        raw = self._request(
            "GET", f"/portfolio/{self.account_id}/positions/0"
        ) or []
        if isinstance(raw, dict):
            raw = [raw]
        result: dict[str, dict] = {}
        for row in raw:
            symbol = row.get("contractDesc") or row.get("symbol")
            if not symbol:
                continue
            result[symbol] = {
                "conid": int(row.get("conid", 0)),
                "quantity": float(row.get("position", 0) or 0),
                "price": float(row.get("mktPrice", 0) or 0),
                "market_value": float(row.get("mktValue", 0) or 0),
                "currency": row.get("currency"),
            }
        return result

    def position_qty(self, symbol: str) -> float:
        return self.positions().get(symbol, {}).get("quantity", 0.0)


class IBKRBroker:
    """Janus broker adapter backed by IBKR."""

    def __init__(self, equity: float, client: IBKRClient) -> None:
        self.equity = equity
        self.client = client
        self.fills: deque[Fill] = deque(maxlen=_FILL_HISTORY_LIMIT)

    def execute(
        self,
        intent: TradeIntent,
        symbol: str,
        price: float,
    ) -> Optional[Fill]:
        if price <= 0:
            logger.warning(
                "non-positive price for %s: %s; skipping", symbol, price
            )
            return None

        if intent.is_flat():
            self._flatten(symbol)
            return None

        target_value = intent.position_size * self.equity
        quantity = target_value / price
        if quantity <= 0:
            logger.warning(
                "non-positive quantity for %s: %s; skipping",
                symbol,
                quantity,
            )
            return None

        try:
            if intent.action is Action.LONG:
                self.client.buy(symbol, quantity)
            elif intent.action is Action.SHORT:
                proxy = SHORT_PROXIES.get(symbol)
                if proxy is None:
                    logger.warning(
                        "no short proxy for %s; skipping SHORT intent",
                        symbol,
                    )
                    return None
                self.client.buy(proxy, quantity)
            else:
                logger.warning(
                    "unknown action %s; skipping", intent.action
                )
                return None
        except IBKRAuthError as exc:
            # A dead session is not transient: no order can be placed
            # until the operator re-authenticates in a browser. Log at
            # CRITICAL and re-raise so the pipeline fails loudly rather
            # than silently skipping trades for hours.
            logger.critical("IBKR session is not authenticated: %s", exc)
            raise
        except RuntimeError as exc:
            logger.error("IBKR order failed for %s: %s", symbol, exc)
            return None

        fill = Fill(
            timestamp=datetime.now(timezone.utc).isoformat(),
            symbol=symbol,
            action=intent.action.value,
            position_size=intent.position_size,
            price=price,
            rationale=intent.rationale,
        )
        self.fills.append(fill)
        return fill

    def _flatten(self, symbol: str) -> None:
        try:
            quantity = self.client.position_qty(symbol)
        except IBKRAuthError as exc:
            logger.critical("IBKR session is not authenticated: %s", exc)
            raise
        except RuntimeError as exc:
            logger.error("could not read position for %s: %s", symbol, exc)
            return
        if quantity > 0:
            try:
                self.client.sell(symbol, quantity)
            except IBKRAuthError as exc:
                logger.critical(
                    "IBKR session is not authenticated: %s", exc
                )
                raise
            except RuntimeError as exc:
                logger.error("could not flatten %s: %s", symbol, exc)
        elif quantity < 0:
            try:
                self.client.buy(symbol, abs(quantity))
            except IBKRAuthError as exc:
                logger.critical(
                    "IBKR session is not authenticated: %s", exc
                )
                raise
            except RuntimeError as exc:
                logger.error(
                    "could not flatten short %s: %s", symbol, exc
                )