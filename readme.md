# JANUS

A dual-mode trading bot that occupies the external-ML role in a modular
AGOP-centred stack.

JANUS consumes four tools, each optional and each behind a stable adapter:

- **AGOP** — the decision engine, either `agop_core.py` (legacy mode) or
  `agop_core_design_by_contract.py` (design-by-contract mode). Ranks
  candidate actions under multi-criteria, strategic, and stochastic
  uncertainty.
- **KAIROS** — the cyclical anomaly filter from `starwalkerz/kairos`.
  Returns a window, a residual amplitude, a flag, and a backend identifier.
- **Causalitybot** — the non-chronological signal from
  `starwalkerz/Causalitybot`. Returns a horizon proxy from the attractor
  strength and a bottleneck proxy from the maximum bottleneck score.
- **An open-source LLM** served over any OpenAI-compatible endpoint
  (Ollama, vLLM, llama.cpp, DeepSeek, Qwen). Consumes Jane Street
  `SKILL.md` bodies as its instruction set.

JANUS never trades without AGOP. The LLM is advisory: it may downsize or
veto a ranked action, never upsize it, never invent one.

---

## Table of Contents

1. Why the external-ML role is the right slot
2. Mathematical specification
3. Strategy profiles
4. Formal invariants
5. The module system
6. Installation
7. Running
8. API
9. Integration patterns
10. Limitations
11. License
12. Appendix A: File tree
13. Appendix B: Glossary
14. Appendix C: References

---

## 1. Why the external-ML role is the right slot

A trading system has four functional layers: data, signal, decision, and
execution. The decision layer is where a language model is useful and where
it is dangerous. Useful because it can read a `SKILL.md` body, weigh a
KAIROS anomaly report against a Causalitybot horizon, and produce a
reasoned veto. Dangerous because a model that can size a position is a
model that can lose the account.

JANUS resolves the tension by giving the LLM exactly one authority:
downward. The deterministic risk engine produces an upper bound on position
size; the LLM may reduce it to zero. This is a formal property, not a policy
statement, and the verifier proves it in Section 4.

The LLM is not the trader. The LLM is not the strategist. The LLM is the
analyst sitting between the deterministic risk engine and the execution
layer, with veto power and no sizing authority above the bound. The
deterministic layers do the arithmetic; the language model does the
interpretation; the verifier enforces the boundary between them.

---

## 2. Mathematical specification

### 2.1 The tick

At each tick the pipeline transforms a market snapshot into a trade intent:

    snapshot → features → PRE_AGOP modules → axes
             → AGOP → POST_AGOP modules → risk bound
             → PRE_LLM modules → LLM → verified intent

The action set is `{LONG, FLAT, SHORT}`. The position size is a fraction of
equity in `[0, position_cap]`, where `position_cap` is the strategy's
absolute ceiling. The pipeline is deterministic given `(snapshot,
configuration, random_seed)` except for the LLM, which is pinned to
temperature zero.

### 2.2 The AGOP decision problem

AGOP ranks a finite set of alternatives under five axes:

    pain, integration, regulatory, readiness, barrier

JANUS constructs the alternatives from the trading action set, populates the
axes from the snapshot, and selects the AGOP mode from the strategy profile.
The axes are computed as follows.

**Pain.** The logistic of twice the absolute signal-to-noise ratio:

    pain(action) = 1 / (1 + exp(-2.0 * |expected_return / realized_volatility|))

The sign of the ratio determines which of LONG or SHORT receives the full
value; the other receives half.

**Integration.** The normalised inverse slippage:

    integration(action) = clip(1.0 - slippage / slippage_maximum, 0.0, 1.0)

FLAT receives a perfect integration score of one, because a flat position
incurs no slippage.

**Regulatory.** The venue risk score, unchanged:

    regulatory(action) = clip(venue_risk, 0.0, 1.0)

FLAT receives zero, because a flat position carries no venue exposure.

**Readiness.** The hyperbolic tangent of twice the signal agreement:

    readiness(LONG) = 0.5 * (1 + tanh(2.0 * signal_agreement))
    readiness(SHORT) = 1 - readiness(LONG)

FLAT receives 0.5, the neutral value.

**Barrier.** The realised volatility normalised against three times itself:

    barrier(action) = clip(realized_volatility / (3.0 * realized_volatility), 0.0, 1.0)

which evaluates to one third for every non-flat action. FLAT receives zero.

In design-by-contract mode, capacity is derived inside AGOP from the
Weisfeiler–Lehman class cardinality and the Shannon entropies of the two
Nash equilibrium strategies. In legacy mode, capacity is supplied in the
theta profile as `legacy_capacity_override`.

### 2.3 The Kelly derivation

Given a binary bet with win probability `p` and payoff ratio `b`, the
growth-optimal fraction of wealth is

    f* = p - (1 - p) / b

**Lemma.** Let wealth evolve as `W → W(1 + fX)`, where `X = +b` with
probability `p` and `X = -1` with probability `1 - p`. The maximiser of
`E[log(1 + fX)]` is the expression above.

**Proof.** The expectation is

    E[log(1 + fX)] = p * log(1 + f * b) + (1 - p) * log(1 - f)

Differentiating with respect to `f`:

    d/df E[log(1 + fX)] = p * b / (1 + f * b) - (1 - p) / (1 - f)

Setting the derivative to zero:

    p * b / (1 + f * b) = (1 - p) / (1 - f)

Cross-multiplying:

    p * b * (1 - f) = (1 - p) * (1 + f * b)

Expanding both sides:

    p * b - p * b * f = 1 - p + f * b - p * f * b

The `p * b * f` terms cancel:

    p * b = 1 - p + f * b

Solving for `f`:

    f = p - (1 - p) / b

The second derivative is strictly negative on the interval `(-1/b, 1)`, so
the stationary point is the unique maximiser. The fraction is clamped to
`[0, 1]` before use. ∎

JANUS computes `p` as the logistic of the signal-to-noise ratio shifted to
`[0.01, 0.99]`, and `b` as the maximum of that ratio and `0.1`. The Kelly
fraction is then multiplied by a strategy-specific coefficient and combined
with the module multiplier.

### 2.4 The risk bound

The upper bound on position size is

    upper_position_size = position_cap
                        × kelly_coefficient
                        × kelly_fraction
                        × module_multiplier

where `module_multiplier ∈ [0, 1]` is the product of every enabled
POST_AGOP module's risk multiplier. A toxic order-flow imbalance forces
`upper_position_size = 0`. The lower-confidence-bound floor and the AGOP
contract check can also force the bound to zero. The final size is the
minimum of the LLM's proposed size and the bound.

### 2.5 The AGOP contract in two modes

Both AGOP cores expose the same surface — `agop(problem) -> State` — but
with different post-conditions.

**Legacy mode.** `Theta` carries `K`; `State` carries `gamma`, `Pi`, `e_1`,
`Sigma`, `T`, `D_star`, `convergence_depth`, `nu_star`, `Y_hat`, `LCB`, `A`,
`Phi`, `R`. No formal verification decorator.

**Design-by-contract mode.** `Theta` has no `K`; `State` additionally
carries `K_derived`, `n_wl_classes`, and `certified()`. The
`verifies_theorem_5` decorator enforces

    depth = 1 ∧ ∀v ∈ R : LCB(v) > 0 ∧ nu*(v) = 1 ∧ Phi(v) > 0

A violation raises `AssertionError` before any state escapes.

JANUS's interpretation of a design-by-contract violation is not a crash. It
is the engine telling the bot that no admissible action exists under the
current snapshot. JANUS maps that outcome deterministically to a flat
intent with zero size.

---

## 3. Strategy profiles

Two profiles; every parameter that differs is named.

| Parameter | Conservative | Aggressive |
|---|---|---|
| `default_agop_mode` | design-by-contract | legacy |
| `theta.pain_threshold` | 0.70 | 0.40 |
| `theta.integration_threshold` | 0.70 | 0.50 |
| `theta.regulatory_threshold` | 0.30 | 0.60 |
| `theta.legacy_capacity_override` | 1 | 3 |
| `lower_confidence_bound_floor` | 0.00 | −0.05 |
| `kelly_coefficient` | 0.25 | 0.60 |
| `position_cap` | 0.10 | 0.35 |
| `toxicity_threshold` | 0.15 | 0.30 |
| `kairos_dampening` | 0.80 | 0.00 |
| `causality_reference_horizon` | 0.60 | 0.30 |
| `causality_gain_coefficient` | 4.0 | 4.0 |
| `llm_confidence_floor` | 0.65 | 0.45 |
| `on_error_default` | fail_closed | fail_open |

The conservative profile is what the design-by-contract AGOP is for: a
contract violation becomes a flat position, the Kelly coefficient is
quarter-Kelly, and the position cap is one tenth of equity. The aggressive
profile accepts the legacy engine's headroom and a looser
lower-confidence-bound floor, and relies on the LLM veto and the toxic-flow
gate for protection.

---

## 4. Formal invariants

The verifier enforces nine invariants on every emitted intent.

**I1 (closed action set).** The action is in the AGOP ranking or is FLAT.

    action ∈ ranking(AGOP) ∪ {FLAT}

**I2 (bounded size).** Position size is in the closed interval from zero to
the strategy's position cap.

    0 ≤ position_size ≤ position_cap

**I3 (contract supremacy).** In design-by-contract mode, an AGOP contract
violation forces action FLAT and size zero.

    (agop_mode = DBC ∧ ¬contract_verified) ⟹ (action = FLAT ∧ position_size = 0)

**I4 (toxicity supremacy).** A toxic order-flow imbalance forces FLAT.

    risk_bound.toxic ⟹ (action = FLAT ∧ position_size = 0)

**I5 (downward-only LLM authority).** Position size never exceeds the risk
bound.

    position_size ≤ risk_bound.upper_position_size

**I6 (determinism).** For fixed inputs, configuration, and random seed, the
intent is identical across runs.

**I7 (module monotone composition).** Every module's risk multiplier is in
`[0, 1]`, so the composed bound never exceeds the base cap.

    ∀module ∈ enabled_modules : 0 ≤ module.risk_multiplier ≤ 1
    ⟹ risk_bound.upper_position_size ≤ position_cap

**I8 (module veto supremacy).** Any enabled module that returns a veto
forces FLAT.

    ∃module ∈ enabled_modules : module.veto ⟹ (action = FLAT ∧ position_size = 0)

**I9 (deterministic composition).** Modules execute alphabetically within
each phase.

    ∀phase : modules_by_phase(phase) = sort(modules_by_phase(phase), key = name)

**Theorem.** The verifier is sound with respect to I1 through I9.

**Proof sketch.** I1 through I6 hold by the base verifier. I7 holds because
`validate_result` rejects any risk multiplier outside `[0, 1]`, and the
product of numbers in `[0, 1]` is in `[0, 1]`. I8 holds because the
orchestrator returns FLAT before constructing a non-flat intent when any
module vetoes. I9 holds because `ModuleRegistry.all_by_phase` sorts
alphabetically. Every emitted intent therefore satisfies all nine
invariants; every intent that would violate one is replaced by the flat
intent, which satisfies them vacuously. ∎

---

## 5. The module system

A module is a deterministic function from a context to a result. It may
patch axes only in the PRE_AGOP phase, may return a risk multiplier in
`[0, 1]`, may veto from any phase, and may contribute structured context
passed to the LLM.

The four built-in modules are:

**kairos.** Runs in POST_AGOP. Calls the `starwalkerz/kairos` core via local
import or HTTP. Contributes a risk multiplier equal to
`1 - dampening * amplitude` when the anomaly is flagged, and `1.0`
otherwise. The dampening coefficient is a strategy parameter; the
aggressive profile sets it to zero, so a flagged anomaly does not change
sizing for that profile.

**causality.** Runs in POST_AGOP. Constructs a fresh
`CausalSetMomentumBot`, feeds it the snapshot history as synthetic order
books, and takes the last signal. The horizon proxy is the attractor
strength; the bottleneck proxy is the maximum bottleneck score divided by
ten and capped at one. Contributes a risk multiplier from the hyperbolic
tangent of `(horizon - reference_horizon) * gain_coefficient`.

**regime.** Runs in PRE_AGOP. Classifies the snapshot into one of three
regimes — calm, normal, choppy — based on the standard deviation of first
differences of the price history. Patches the barrier and readiness axes
accordingly.

**sentiment.** Runs in PRE_AGOP. Reads `snapshot.external_data["sentiment"]`
as a float in `[-1, 1]`. Patches the pain and readiness axes accordingly.
No-op if the key is absent.

Custom modules are registered by importing a Python path specified in the
configuration's `module_imports` list. The imported module must export a
`module` variable that is a `Module` instance.

---

## 6. Installation

### 6.1 Requirements

- Python 3.10 or later
- No native compilation
- No GPU

### 6.2 Dependencies

Install the Python dependencies:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

The dependencies are:

- `numpy` for numerical operations
- `scipy` for statistical functions
- `pandas` for tabular data
- `httpx` for HTTP calls to the LLM and to remote adapters
- `fastapi` for the REST API
- `uvicorn` for the ASGI server
- `pydantic` for the request and response schemas
- `tomli` for TOML configuration parsing
- `pyyaml` for the SKILL.md frontmatter
- `pytest` for the test suite

### 6.3 Optional upstream tools

The AGOP engine, KAIROS anomaly detector, and Causalitybot signal generator
are optional at the dependency level. Each is loaded via import; if the
corresponding directory is not on `PYTHONPATH`, or the corresponding HTTP
endpoint is not configured, the adapter for that tool returns an
unavailable result and the pipeline falls back to AGOP alone.

### 6.4 The LLM

Any OpenAI-compatible endpoint works. Ollama is the simplest:

```bash
ollama pull qwen2.5:7b-instruct
ollama serve
```

Then set the following in `config.toml`:

```toml
[llm]
base_url = "http://localhost:11434/v1"
model = "qwen2.5:7b-instruct"
api_key = "ollama"
temperature = 0.0
timeout_s = 30.0
```

vLLM, llama.cpp server, DeepSeek, and Qwen all expose the same
`/v1/chat/completions` shape and work identically.

### 6.5 Verification

Run the test suite:

```bash
python -m pytest tests/ -q
```

The tests cover the verifier invariants, the AGOP bridge, the risk bound
computation, the orchestrator pipeline, and the module lifecycle.

---

## 7. Running

### 7.1 Server and web interface

```bash
python run.py
```

The server binds to `http://127.0.0.1:8400` by default. Open that URL in a
browser to access the web interface. The interface exposes a strategy
selector, an AGOP mode selector, a model selector, a module toggle panel, a
market snapshot panel, and a live audit log.

OpenAPI documentation is available at `http://127.0.0.1:8400/docs`.

### 7.2 Command line

Run a single tick:

```bash
python cli.py tick --strategy conservative --agop-mode dbc
```

Disable specific modules for one run:

```bash
python cli.py tick --strategy aggressive --disable sentiment regime
```

The CLI prints the full tick record as JSON, identical in structure to the
API response.

### 7.3 Configuration file

Copy `config.example.toml` to `config.toml` and edit it. The configuration
file has the following sections:

- `[strategy]` — the strategy name
- `[agop]` — the AGOP mode and the local path or HTTP URL
- `[kairos]` — the KAIROS local path or HTTP URL, and whether to use the
  quantum path
- `[causality]` — the Causalitybot local path or HTTP URL
- `[llm]` — the OpenAI-compatible endpoint, model, key, temperature, and
  timeout
- `[skills]` — the SKILL.md directory and the active skill names
- `[risk]` — the equity and the random seed
- `[modules]` — per-module enabled flag and on_error policy, plus the list
  of custom module imports

---

## 8. API

The API is served by FastAPI. All endpoints return JSON unless otherwise
noted.

| Method | Path | Description |
|---|---|---|
| GET | `/` | Web interface |
| GET | `/api/health` | Health and adapter status |
| GET | `/api/config` | Current configuration |
| POST | `/api/config` | Update strategy and AGOP mode |
| GET | `/api/modules` | List registered modules |
| POST | `/api/modules/{name}/toggle` | Enable or disable a module |
| POST | `/api/modules/{name}/on_error` | Set a module's on_error policy |
| POST | `/api/tick` | Run one tick on a supplied snapshot |
| GET | `/api/audit` | Recent intents with rationales |
| WS | `/ws/stream` | Continuous ticks |

### 8.1 `POST /api/tick`

Request body:

```json
{
  "symbol": "BTC/USDT",
  "price": 50000.0,
  "expected_return": 0.004,
  "realized_volatility": 0.012,
  "slippage": 2.0,
  "slippage_maximum": 20.0,
  "venue_risk": 0.2,
  "signal_agreement": 0.6,
  "order_flow_imbalance": 0.05,
  "history": [50000.0, 50010.0, 49980.0],
  "timestamps": [0.0, 1.0, 2.0],
  "external_data": { "sentiment": 0.2 }
}
```

Response body:

```json
{
  "snapshot": {},
  "agop": {
    "mode": "dbc",
    "ranking": ["LONG", "FLAT", "SHORT"],
    "contract_verified": true,
    "contract_error": null,
    "capacity": 3,
    "number_of_weisfeiler_lehman_classes": 3
  },
  "risk": {
    "upper_position_size": 0.032,
    "kelly_fraction": 0.52,
    "module_multiplier": 0.80,
    "toxic": false,
    "reason": "kelly=0.5200 coefficient=0.25 module_multiplier=0.8000 cap=0.10"
  },
  "intent": {
    "action": "LONG",
    "position_size": 0.024,
    "rationale": "Regime is trending per KAIROS and Causalitybot",
    "agop_mode": "dbc",
    "strategy": "conservative",
    "skills_cited": ["regime-classifier", "sizing-discipline"],
    "vetoed": false,
    "contract_forced_flat": false
  },
  "fill": {}
}
```

### 8.2 `POST /api/config`

Request body:

```json
{
  "strategy": "conservative",
  "agop_mode": "dbc",
  "llm_model": "qwen2.5:7b-instruct"
}
```

Any field may be omitted; the missing fields retain their current values.

### 8.3 `POST /api/modules/{name}/toggle`

Request body:

```json
{ "enabled": false }
```

Disables the named module for all subsequent ticks.

### 8.4 `WS /ws/stream`

Send `{"type": "tick", "snapshot": {}}` with the same snapshot schema as
`POST /api/tick`. The server responds with the full tick record on each
message.

---

## 9. Integration patterns

The adapter layer treats AGOP, KAIROS, and Causalitybot as opaque
interfaces. Nothing in JANUS assumes their internals; the modules wrap
their public surface.

**Pattern A — AGOP upstream of the pipeline.** The default: AGOP ranks the
trading action set, and JANUS trades the top-ranked action under the risk
bound and the LLM veto.

**Pattern B — KAIROS validates the AGOP window.** If AGOP's ranking is
already suspect (for example, because the axes were constructed from a
snapshot with poor data quality), KAIROS's anomaly flag can dampen the
risk bound before the LLM sees it.

**Pattern C — Causalitybot overrides AGOP.** In the aggressive profile, the
Causalitybot gain can dominate the risk multiplier. When the causal horizon
is strong, the multiplier approaches one. When it is weak, it approaches
zero. The practical effect is that the pipeline trades only when both AGOP
and the causal signal agree.

**Pattern D — custom modules plug in without code changes.** A user can add
a module by placing its Python file anywhere on `PYTHONPATH`, adding the
path to the `module_imports` list in `config.toml`, and exporting a
`module` variable from that file. The new module is registered on the next
startup and appears in the web interface's module panel.

---

## 10. Limitations

**Paper execution only.** `execution.py` ships a paper broker. A live
broker adapter is out of scope; the interface is documented and the paper
broker can be swapped for a live one by implementing `PaperBroker.execute`.

**The LLM is audited for authority, not correctness.** The verifier
enforces that the LLM's size does not exceed the risk bound. The verifier
does not enforce that the LLM's rationale is correct, that the LLM's cited
skills are the right ones, or that the LLM's action is better than the
AGOP top-ranked action. A model that produces a confident wrong rationale
is still bounded by the risk bound; a model that is right but timid will
undersize.

**AGOP's axis-construction limitation propagates.** If the axes constructed
from the snapshot are wrong — because `expected_return` is miscalibrated,
because `realized_volatility` is stale, because `signal_agreement` does not
reflect the current signal — the ranking is wrong. The AGOP README's
garbage-in warning applies to JANUS in full.

**KAIROS and Causalitybot are optional.** If either is absent from
`PYTHONPATH` and no HTTP URL is configured, the corresponding module returns
a neutral result and the pipeline runs on AGOP and the toxic-flow gate
alone. The risk multipliers from the absent modules are set to one, which
leaves the bound unchanged.

**The quantum path in KAIROS is optional and off by default.** Enabling
`kairos_quantum = true` requires a Qiskit installation and an IQM API
token. Without those, the module uses the classical amplitude estimate and
reports `backend = "classical"` in the KAIROS context.

**Not investment advice.** JANUS is research software. It has been tested
against synthetic snapshots and against the reference instances of the
tools it consumes. It has not been tested against live market data, and
its behaviour on adversarial order books is unknown.

**The regime classifier is a proxy.** `regime.py` classifies the market from
the standard deviation of price first differences. This is not a causal
regime classifier; it is a volatility proxy. Real regime classification
requires order book microstructure, which JANUS does not consume in the
reference implementation.

**The sentiment module is a placeholder.** `sentiment.py` reads a single
float from `external_data["sentiment"]`. It does not call any sentiment
provider. A production deployment should replace it with a module that
consumes a real sentiment feed and returns a properly calibrated signal.

---

## 11. License

MIT.

---

## Appendix A: File tree

```
janus/
├── README.md
├── requirements.txt
├── pyproject.toml
├── config.example.toml
├── run.py
├── cli.py
├── janus/
│   ├── __init__.py
│   ├── contracts.py
│   ├── config.py
│   ├── skills.py
│   ├── llm.py
│   ├── agop_bridge.py
│   ├── features.py
│   ├── strategies.py
│   ├── risk.py
│   ├── execution.py
│   ├── bootstrap.py
│   ├── orchestrator.py
│   ├── api.py
│   ├── ui.html
│   └── modules/
│       ├── __init__.py
│       ├── base.py
│       ├── registry.py
│       ├── kairos.py
│       ├── causality.py
│       ├── regime.py
│       └── sentiment.py
├── skills/
│   ├── toxic-flow-gate/SKILL.md
│   ├── regime-classifier/SKILL.md
│   └── sizing-discipline/SKILL.md
└── tests/
    ├── test_contracts.py
    ├── test_agop_bridge.py
    ├── test_risk.py
    ├── test_orchestrator.py
    └── test_modules.py
```

## Appendix B: Glossary

**AGOP** — Attributed-Graph Operator Pipeline. A computable decision
engine that composes graph-theoretic, game-theoretic, systems-theoretic,
topological, deductive, stochastic, and probabilistic operators into a
single typed directed acyclic graph. Two modes: legacy (exogenous capacity)
and design-by-contract (endogenous capacity with verification decorator).

**Causalitybot** — A non-chronological signal generator that identifies
causal horizons and bottlenecks in order flow. Consumed by JANUS via the
`causality` module.

**Contract** — In the design-by-contract AGOP mode, the set of
post-conditions enforced by the `verifies_theorem_5` decorator. In JANUS,
the set of invariants I1 through I9 enforced by the `verify_trade_intent`
decorator.

**KAIROS** — A cyclical anomaly detector that identifies deviations from a
declared cycle. Consumed by JANUS via the `kairos` module.

**Kelly fraction** — The growth-optimal position fraction for a binary bet,
computed as `f* = p - (1 - p) / b` and clamped to `[0, 1]`.

**LLM** — Large language model. Served over an OpenAI-compatible endpoint.
Consumed by JANUS as the analyst with downward-only sizing authority.

**Module** — A deterministic function from a context to a result. Runs in
one of three phases. May patch axes, contribute a risk multiplier, veto,
or contribute context.

**Phase** — One of PRE_AGOP, POST_AGOP, PRE_LLM. Determines when a module
executes in the pipeline.

**Toxic flow** — An order-flow imbalance against the intended action
direction. Forces a flat intent via invariant I4.

**Verifier** — The `verify_trade_intent` decorator that enforces invariants
I1 through I9 on every emitted intent.

## Appendix C: References

The Jane Street agent_skills reference: `https://github.com/janestreet/agent_skills`

The AGOP repository: `https://github.com/starwalkerz/AGOP`

The KAIROS repository: `https://github.com/starwalkerz/kairos`

The Causalitybot repository: `https://github.com/starwalkerz/Causalitybot`

The Brassard–Høyer–Mosca–Tapp 2002 paper on quantum amplitude estimation,
which the KAIROS quantum path implements.

The Kelly 1956 paper on optimal betting, from which the risk bound
derivation in Section 2.3 follows.

The Nash 1950 paper on equilibrium points, which the AGOP ranking phase
consumes.