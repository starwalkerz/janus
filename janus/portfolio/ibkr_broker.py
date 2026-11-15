"""janus.portfolio.ibkr_broker — IBKR implementation of ``PaperBroker.execute``.

Not a Janus module. It is the live-broker extension point documented in
``janus/execution.py``.

Semantics:

- ``FLAT``  -> flatten (long or short); return ``None``.
- ``LONG``  -> buy ``position_size * equity / price`` shares; return ``Fill``.
- ``SHORT`` -> buy inverse-ETF proxy in ``SHORT_PROXIES``; log and return
               ``None`` if no proxy.

Known limitations
-----------------
- ``self.equity`` captured at construction. Set ``broker.equity`` before
  ``execute`` if it has changed.
- ``Fill.action`` uses ``intent.action.value``. Verify against
  ``janus/execution.py`` before deployment.
- On ``SHORT``, ``Fill`` records the intent symbol, not the proxy.

Requires ``requests``. Install from ``requirements.txt`` or
``pip install "requests>=2.32"``.
"""

from __future__ import annotations

import logging
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


class IBKRClient:
    """Minimal HTTP client for the IBKR Client Portal Web API."""

    def __init__(
        self,
        account_id: str,
        gateway: str = "https://localhost:5000",
        verify_ssl: bool = False,
        timeout: int = 30,
        state_dir: str | Path = "./state",
    ) -> None:
        self.account_id = account_id
        self.base = f"{gateway.rstrip('/')}/v1/api"
        self.verify = verify_ssl
        self.timeout = timeout
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self._conid_cache_path = self.state_dir / "conid_cache.json"
        self._conid_cache: dict[str, int] = self._load_cache()

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

    def _request(self, method: str, path: str, params=None, body=None):
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
        except RuntimeError as exc:
            logger.error("could not read position for %s: %s", symbol, exc)
            return
        if quantity > 0:
            try:
                self.client.sell(symbol, quantity)
            except RuntimeError as exc:
                logger.error("could not flatten %s: %s", symbol, exc)
        elif quantity < 0:
            try:
                self.client.buy(symbol, abs(quantity))
            except RuntimeError as exc:
                logger.error(
                    "could not flatten short %s: %s", symbol, exc
                )