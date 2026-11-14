"""
modules/opportunity_synthesizer.py — synthesize the opportunity signals.

Runs in PRE_LLM. Reads prior results (both PRE_AGOP and POST_AGOP) and
produces structured context for the LLM indicating whether the
opportunity signals agree.

Consensus values:
    "unanimous"  — ≥ 2 modules qualify, all agree on direction
    "single"     — 1 module qualifies
    "mixed"      — ≥ 2 modules qualify with conflicting directions
    "none"       — 0 modules qualify

Confidence:
    len(qualifying) / 3                    if unanimous
    0.5                                    if single
    0.0                                    if mixed or none

The synthesizer never vetoes. It only provides context.
"""

from __future__ import annotations

from janus.contracts import Action, ModulePhase
from janus.modules.base import Module, ModuleContext, ModuleResult


OPPORTUNITY_MODULES = (
    "agop_opportunity",
    "causality_opportunity",
    "kairos_opportunity",
)


class OpportunitySynthesizerModule(Module):
    name = "opportunity_synthesizer"
    phase = ModulePhase.PRE_LLM

    def __init__(self, configuration=None) -> None:
        pass

    def run(self, context: ModuleContext) -> ModuleResult:
        qualifying: list[tuple[str, Action]] = []

        for name in OPPORTUNITY_MODULES:
            result = context.prior_results.get(name)
            if result is None:
                continue
            if not result.context:
                continue
            inner = result.context.get(name, {})
            if not inner.get("qualified", False):
                continue
            direction_value = inner.get("direction")
            if direction_value is None:
                continue
            try:
                direction = Action(direction_value)
            except ValueError:
                continue
            qualifying.append((name, direction))

        if not qualifying:
            return ModuleResult(
                name=self.name,
                phase=self.phase,
                context={
                    "opportunity_synthesis": {
                        "consensus": "none",
                        "direction": None,
                        "confidence": 0.0,
                        "contributing_modules": [],
                    }
                },
                notes="opportunity_synthesis: no qualifying opportunities",
            )

        directions = {direction for _, direction in qualifying}
        module_names = sorted(name for name, _ in qualifying)

        if len(directions) == 1:
            direction = next(iter(directions))
            if len(qualifying) >= 2:
                consensus = "unanimous"
                confidence = len(qualifying) / len(OPPORTUNITY_MODULES)
            else:
                consensus = "single"
                confidence = 0.5
        else:
            direction = None
            consensus = "mixed"
            confidence = 0.0

        synthesis = {
            "consensus": consensus,
            "direction": direction.value if direction else None,
            "confidence": float(confidence),
            "contributing_modules": module_names,
        }

        return ModuleResult(
            name=self.name,
            phase=self.phase,
            context={"opportunity_synthesis": synthesis},
            notes=(
                f"opportunity_synthesis: consensus={consensus} "
                f"direction={direction.value if direction else 'mixed'} "
                f"confidence={confidence:.2f} "
                f"modules={','.join(module_names)}"
            ),
        )