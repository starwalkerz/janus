"""
execution.py — paper broker.

Orders are recorded with the intent that produced them, so the audit log is
a complete reconstruction of every decision.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from janus.contracts import TradeIntent


@dataclass
class Fill:
    timestamp: str
    symbol: str
    action: str
    position_size: float
    price: float
    rationale: str


@dataclass
class PaperBroker:
    equity: float
    position: float = 0.0
    fills: list[Fill] = field(default_factory=list)

    def execute(
        self,
        intent: TradeIntent,
        symbol: str,
        price: float,
    ) -> Fill | None:
        if intent.is_flat():
            self.position = 0.0
            return None
        signed_position = (
            intent.position_size
            if intent.action.value == "LONG"
            else -intent.position_size
        )
        self.position = signed_position * self.equity / price
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