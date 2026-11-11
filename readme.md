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

The stack also includes two optional quantum econophysics modules that run
on IQM Resonance when configured, fall back to Qiskit Aer when Qiskit is
installed, and fall back to exact classical evolution otherwise.

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
11. Quantum econophysics modules
12. License
13. Appendix A: File tree
14. Appendix B: Glossary
15. Appendix C: References

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

The `econophysics_tunneling` module, when enabled, replaces the static
one-third barrier with a physical barrier-penetration probability computed
on a quantum circuit. See Section 11.

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
| `econophysics_herding_sensitivity` | 0.5 | 0.2 |

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

The six built-in modules are:

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

**econophysics_tunneling.** Runs in PRE_AGOP. Encodes the nearest heavy-
volume barrier as a potential on a discretized Baaquie Hamiltonian, evolves
the price state through the barrier, and patches AGOP's `barrier` axis from
the resulting tunneling probability. See Section 11.

**econophysics_herding.** Runs in POST_AGOP. Encodes cross-asset return
correlations as an Ising cost Hamiltonian and runs QAOA to measure the
magnetization order parameter. Contributes a risk multiplier
`1 - sensitivity * |M|`, where `sensitivity` is a strategy parameter. See
Section 11.

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

The core dependencies are:

- `numpy` for numerical operations
- `scipy` for statistical functions and the classical quantum fallback
- `pandas` for tabular data
- `httpx` for HTTP calls to the LLM and to remote adapters
- `fastapi` for the REST API
- `uvicorn` for the ASGI server
- `pydantic` for the request and response schemas
- `tomli` for TOML configuration parsing
- `pyyaml` for the SKILL.md frontmatter
- `pytest` for the test suite

### 6.3 Optional quantum dependencies

The econophysics modules run on IQM Resonance when the following packages
are installed and an API token is configured:

```bash
pip install qiskit qiskit-aer iqm-client
```

Without these packages, the modules fall back to exact classical evolution
via `scipy.sparse.linalg.expm_multiply`, which is mathematically equivalent
for the circuit sizes JANUS uses (up to 8 qubits). Installing the quantum
packages adds roughly 500 MB to the environment. The classical fallback
produces the same structural result, with the `backend` field in each
module's context set to `classical-exact` instead of `iqm:*` or
`qiskit-aer`.

### 6.4 Optional upstream tools

The AGOP engine, KAIROS anomaly detector, and Causalitybot signal generator
are optional at the dependency level. Each is loaded via import; if the
corresponding directory is not on `PYTHONPATH`, or the corresponding HTTP
endpoint is not configured, the adapter for that tool returns an
unavailable result and the pipeline falls back to AGOP alone.

### 6.5 The LLM

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

### 6.6 Verification

Run the test suite:

```bash
python -m pytest tests/ -q
```

The tests cover the verifier invariants, the AGOP bridge, the risk bound
computation, the orchestrator pipeline, the module lifecycle, and the
econophysics modules' Hamiltonian symmetry, barrier detection, and risk
multiplier bounds.

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
- `[quantum]` — the IQM token, server, backend, and per-circuit parameters
  for the econophysics modules
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

For the herding module to consume real cross-asset correlations, include
`external_data["econophysics_assets"]` as a dict mapping asset name to a
list of prices. Without it, the module falls back to a multi-horizon
momentum alignment measure computed from the single-asset history.

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
  "fill": {},
  "modules": {
    "pre_agop": {
      "econophysics_tunneling": {
        "name": "econophysics_tunneling",
        "phase": "pre_agop",
        "axes_patch": { "barrier": { "LONG": 0.35, "SHORT": 0.5 } },
        "risk_multiplier": 1.0,
        "veto": false,
        "context": {
          "econophysics_tunneling": {
            "direction": "up",
            "barrier_price": 50500.0,
            "tunneling_probability": 0.65,
            "effective_barrier": 0.35,
            "backend": "qiskit-aer"
          }
        },
        "notes": "tunneling: direction=up P_tunnel=0.6500 barrier=0.3500 backend=qiskit-aer"
      }
    },
    "post_agop": {
      "econophysics_herding": {
        "name": "econophysics_herding",
        "phase": "post_agop",
        "risk_multiplier": 0.75,
        "veto": false,
        "context": {
          "econophysics_herding": {
            "magnetization": 0.5,
            "signed_magnetization": 0.5,
            "cost": -1.25,
            "risk_multiplier": 0.75,
            "layers": 1,
            "backend": "qiskit-aer",
            "converged": true
          }
        },
        "notes": "herding: |M|=0.5000 multiplier=0.7500 backend=qiskit-aer"
      }
    }
  }
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

The adapter layer treats AGOP, KAIROS, Causalitybot, and the quantum
econophysics modules as opaque interfaces. Nothing in JANUS assumes their
internals; the modules wrap their public surface.

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

**Pattern D — Econophysics patches the barrier and shrinks size.** The
tunneling module replaces AGOP's static one-third barrier constant with a
physical tunneling probability computed from the current volume profile.
The herding module shrinks position size when cross-asset correlations
indicate a ferromagnetic consensus. The two effects act in different
phases and cannot collide under the current invariants.

**Pattern E — custom modules plug in without code changes.** A user can add
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

**The quantum path is optional and off by default in effect.** The
econophysics modules run on IQM Resonance only when `quantum_iqm_token` is
set and the `qiskit` and `iqm-client` packages are installed. Without
those, the modules use Qiskit Aer (when Qiskit is installed) or exact
classical evolution (always available), and record the backend in the
context field.

**The quantum path is slower than the classical fallback.** On the problem
sizes JANUS handles (4 to 8 qubits), the classical exact fallback is
faster than submitting to IQM hardware and produces the same result. The
quantum path matters when the circuit size exceeds the reach of classical
matrix exponentiation (roughly 12 qubits), which is beyond the current
configuration and beyond the coherence budget of current NISQ hardware.
The quantum path is provided for research and for the theoretical
correctness of the algorithm's physical interpretation, not because it
outperforms the classical fallback at these sizes.

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

## 11. Quantum econophysics modules

JANUS ships two quantum econophysics modules that run on IQM Resonance
when an API token is configured, fall back to Qiskit Aer when Qiskit is
installed but IQM is not, and fall back to exact classical evolution when
neither is available.

### 11.1 Baaquie tunneling

The `econophysics_tunneling` module runs in `PRE_AGOP`. It encodes the
nearest heavy-volume support or resistance level as a potential barrier
on a discretized Baaquie Hamiltonian, evolves the current log-price state
through the barrier for a short evolution window, and measures the
probability of finding the system strictly beyond the barrier.

**Baaquie Hamiltonian.** On a log-price lattice of dimension \(N = 2^n\)
with spacing \(h\), the discretized Black–Scholes Hamiltonian is

\[
H_{BS} = -\frac{\sigma^2}{2} \frac{\partial^2}{\partial x^2}
       + \left(\frac{\sigma^2}{2} - r\right) \frac{\partial}{\partial x} + r.
\]

The kinetic term becomes tight-binding hopping \(-t_{\text{hop}} \sum_j
(|j+1\rangle\langle j| + \text{h.c.})\). The drift term becomes a small
asymmetric hopping correction. Adding a barrier potential
\(V(x) = V_0 \exp(-(x - x_B)^2 / (2 w^2))\) gives

\[
H = H_{\text{kin}} + V, \qquad
P_{\text{tunnel}}(t) = \|\Pi_{\text{out}} e^{-i H t} |x_0\rangle\|^2.
\]

**Theorem (Trotter approximation).** Let \(U(t) = e^{-i H t}\) and let
\(U_S(t, m) = [e^{-i T t/m} e^{-i V t/m}]^m\) be the first-order
Suzuki–Trotter product. Then

\[
\|U(t) - U_S(t, m)\| \leq \frac{t^2}{2m} \|[T, V]\|.
\]

*Proof.* The Baker–Campbell–Hausdorff expansion of \(e^{-i T \tau}
e^{-i V \tau}\) is \(e^{-i(T+V)\tau - \frac{\tau^2}{2}[T,V] +
O(\tau^3)}\). The leading error per step is \(\frac{\tau^2}{2}[T, V]\).
Compounding \(m\) steps with \(\tau = t/m\) gives the stated bound after
absorbing higher-order terms. The bound is standard and is the reason
Qiskit's `PauliEvolutionGate` with `LieTrotter(reps=m)` produces a
circuit whose output converges to the exact evolution as \(m\) grows. ∎

**Axis patch.** The module patches AGOP's `barrier` axis. High tunneling
probability means the wall is porous, so the effective barrier is set low:
`barrier_effective = clip(1 - P_tunnel, 0.05, 0.95)`. The direction of
the barrier (up for resistance, down for support) determines which of
`LONG` or `SHORT` receives the patch; the other side keeps the neutral
0.5. This replaces AGOP's static one-third constant with a genuine
physical barrier-penetration probability.

**Direction selection.** The module computes the nearest barrier above
and the nearest support below the current price from the volume profile
of the snapshot history. It selects the direction whose barrier is closer
in log-price space. If neither exists, the module returns a neutral
result and the pipeline proceeds without the patch.

### 11.2 Ising herding

The `econophysics_herding` module runs in `POST_AGOP`. It encodes the
pairwise return correlation between assets (or, in the single-asset
fallback, between overlapping history windows) as an Ising cost
Hamiltonian, runs QAOA at shallow depth, and measures the magnetization
order parameter \(M\).

**Cost Hamiltonian.**

\[
H_C = -\sum_{i<j} J_{ij} Z_i Z_j - \sum_i h_i Z_i.
\]

\(J_{ij}\) is the clipped Pearson correlation of log-returns between
asset \(i\) and asset \(j\). \(h_i\) is the hyperbolic tangent of the
asset's mean log-return scaled by 100, which is a momentum drift proxy.
The mixer is \(H_M = \sum_i X_i\).

**Theorem (magnetization as herding measure).** Let
\(|\psi(\beta, \gamma)\rangle = \prod_{k=1}^p e^{-i \beta_k H_M}
e^{-i \gamma_k H_C} |+\rangle^n\) be the QAOA state at depth \(p\). The
magnetization

\[
M(\beta, \gamma) = \frac{1}{n} \sum_{i=1}^n
\langle \psi(\beta, \gamma) | Z_i | \psi(\beta, \gamma)\rangle
\]

satisfies \(|M| \leq 1\), with equality if and only if the state is a
computational basis state (fully ferromagnetic) and \(M = 0\) if and only
if the state is uniform over the computational basis (paramagnetic).

*Proof.* Each \(Z_i\) has eigenvalues \(\pm 1\), so \(|\langle Z_i \rangle|
\leq 1\) for any state. If the state is a single basis state \(|b\rangle\),
then \(\langle Z_i \rangle = \pm 1\) for every \(i\), so \(|M| = 1\). If the
state is uniform, each \(\langle Z_i \rangle = 0\) by symmetry, so \(M = 0\).
The intermediate values interpolate. ∎

**Risk multiplier.** The module returns \(1 - \alpha |M|\), with
\(\alpha = 0.5\) for the conservative profile and \(\alpha = 0.2\) for the
aggressive profile. In a herding phase (\(|M|\) close to one), position
size shrinks; in a disordered phase (\(|M|\) close to zero), position size
is unaffected.

**Correlation source.** The module reads `snapshot.external_data["econophysics_assets"]`
when present. The value must be a dict mapping asset name to a list of
prices. When absent, the module splits the single-asset history into
overlapping windows and computes correlations between windows. The
fallback is a multi-horizon momentum alignment measure, not a cross-asset
herding measure; the module records the distinction in its `notes` field
so the LLM can interpret it correctly.

### 11.3 Backend selection

Each module queries the quantum runner with a preference order:

1. **IQM Resonance** — when `quantum_iqm_token` is set, the circuit is
   transpiled for the requested backend (the provider default if
   `quantum_iqm_backend` is empty) and submitted via
   `backend.run(circuit, shots=N)`.
2. **Qiskit Aer** — when Qiskit is installed but no token is available,
   the same circuit runs on the Aer statevector simulator.
3. **Classical exact** — when Qiskit is not installed, the same
   Hamiltonian is exponentiated via `scipy.sparse.linalg.expm_multiply`.

Every path returns the same structural result: a probability vector for
the tunneling circuit, and a `magnetization` plus `cost` for the QAOA
circuit. The `backend` field in each result records which path was taken,
so the audit log preserves provenance.

The classical fallback is exact, not approximate, for both circuits: the
tunneling probability is the exact modulus squared of the evolved
amplitude, and the QAOA magnetization is the exact expectation value
under the optimised (beta, gamma) parameters. The IQM and Aer paths
introduce sampling noise (from shots) and Trotter error (from circuit
depth). The `backend` field distinguishes the three cases so a reader can
tell whether the reported number is exact or sampled.

### 11.4 Two modules, not one

The tunneling effect is a barrier patch, which JANUS permits only in
`PRE_AGOP` (invariant I7). The herding effect is a risk multiplier, which
JANUS permits only in `POST_AGOP` (invariant I9). A single module cannot
legally do both. The two modules share the quantum runner and the
correlation extractor but run in different phases, and each contributes
its effect through the mechanism that the phase permits. This is the
cleanest decomposition consistent with the invariants.

### 11.5 Parameters and their meanings

The two modules expose ten parameters, all with defaults that work on a
four-qubit IQM processor:

| Parameter | Default | Meaning |
|---|---|---|
| `quantum_iqm_token` | `""` | IQM Resonance API token; empty disables IQM path |
| `quantum_iqm_server` | `"https://resonance.iqm.tech"` | IQM Resonance endpoint |
| `quantum_iqm_backend` | `""` | Specific IQM backend; empty uses provider default |
| `quantum_tunneling_qubits` | `4` | Lattice size is \(2^n\); 4 qubits = 16 price levels |
| `quantum_tunneling_time` | `3.0` | Evolution window in circuit time units |
| `quantum_tunneling_trotter_steps` | `3` | Suzuki–Trotter repetition count |
| `quantum_herding_qubits` | `4` | Number of assets or history windows |
| `quantum_herding_layers` | `1` | QAOA depth |
| `quantum_herding_shots` | `4000` | Shots per QAOA cost evaluation |

The default parameters produce a tunneling circuit of depth approximately
30 with three Trotter steps, and a QAOA circuit of depth approximately 10
per layer. Both are well within the coherence budget of the IQM Garnet
processor (20 qubits) at current gate fidelities.

### 11.6 Cost and latency

The tunneling circuit runs once per tick. On IQM Resonance, that is one
quantum job per tick, which is one to four credits depending on backend
availability. On Aer, it is a fraction of a second of CPU. On classical
exact, it is a matrix exponential of dimension 16, which is
sub-millisecond.

The QAOA circuit runs `optimizer_iterations` (default 60) times per tick
for the classical optimisation loop, plus one final evaluation. On IQM
Resonance, that is 61 quantum jobs per tick, which is 61 to 244 credits.
**This is prohibitive for live trading on IQM Resonance without a
research budget.** Aer and classical exact complete in seconds.

For live deployment on IQM Resonance, the recommended configuration is:

- Run the tunneling circuit on IQM per tick.
- Run the herding circuit on Aer or classical exact per tick, with
  periodic IQM validation at lower frequency (for example, once per
  hour or once per day).
- Set `quantum_herding_shots` to a lower value (1000) to keep the Aer
  path fast.
- Keep `quantum_herding_layers = 1`. Depth 2 multiplies the circuit
  cost by four with diminishing returns on the magnetization estimate.

### 11.7 Determinism

The tunneling circuit is deterministic given a seed and a backend: the
initial state is a basis state, the evolution is a fixed unitary, and the
shots are reproducible under Aer's seeded simulator. On IQM hardware the
shots are hardware-random, so the reported `P_tunnel` will vary slightly
between runs. To make the full pipeline reproducible end-to-end, use
`quantum_iqm_token = ""` (forcing the Aer path) with `random_seed = 42`,
which is the default.

The QAOA circuit is deterministic under Aer because the COBYLA optimiser
starts from a seeded initial point (`random_seed = 42` in the runner) and
the cost evaluations are seeded. Under IQM hardware, the shots are
hardware-random and the optimiser follows a different trajectory on
different runs.

The `econophysics_tunneling` and `econophysics_herding` modules include
the `backend` field in their context dict, so a downstream auditor can
distinguish a hardware run from an Aer run from a classical run. The
JANUS audit log preserves the context dict per tick.

---

## 12. License

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
│       ├── sentiment.py
│       ├── quantum_runner.py
│       └── econophysics.py
├── skills/
│   ├── toxic-flow-gate/SKILL.md
│   ├── regime-classifier/SKILL.md
│   ├── sizing-discipline/SKILL.md
│   └── econophysics-analyst/SKILL.md
└── tests/
    ├── test_contracts.py
    ├── test_agop_bridge.py
    ├── test_risk.py
    ├── test_orchestrator.py
    ├── test_modules.py
    └── test_econophysics.py
```

## Appendix B: Glossary

**AGOP** — Attributed-Graph Operator Pipeline. A computable decision
engine that composes graph-theoretic, game-theoretic, systems-theoretic,
topological, deductive, stochastic, and probabilistic operators into a
single typed directed acyclic graph. Two modes: legacy (exogenous capacity)
and design-by-contract (endogenous capacity with verification decorator).

**Baaquie Hamiltonian** — The discretized Black–Scholes Hamiltonian
expressed as a quantum operator on a log-price lattice. Basis for the
tunneling module.

**Causalitybot** — A non-chronological signal generator that identifies
causal horizons and bottlenecks in order flow. Consumed by JANUS via the
`causality` module.

**Contract** — In the design-by-contract AGOP mode, the set of
post-conditions enforced by the `verifies_theorem_5` decorator. In JANUS,
the set of invariants I1 through I9 enforced by the `verify_trade_intent`
decorator.

**Econophysics** — The application of physics methods, including quantum
mechanics and statistical mechanics, to economic and financial systems.
The two modules `econophysics_tunneling` and `econophysics_herding` apply
the Baaquie Hamiltonian and the Ising model respectively.

**Ising Hamiltonian** — The cost Hamiltonian \(H_C = -\sum_{i<j} J_{ij} Z_i Z_j
- \sum_i h_i Z_i\) used to encode cross-asset correlations. Basis for the
herding module.

**KAIROS** — A cyclical anomaly detector that identifies deviations from a
declared cycle. Consumed by JANUS via the `kairos` module.

**Kelly fraction** — The growth-optimal position fraction for a binary bet,
computed as `f* = p - (1 - p) / b` and clamped to `[0, 1]`.

**LLM** — Large language model. Served over an OpenAI-compatible endpoint.
Consumed by JANUS as the analyst with downward-only sizing authority.

**Magnetization** — The order parameter \(M = (1/n) \sum_i \langle Z_i \rangle\)
of a QAOA state on the Ising cost Hamiltonian. Measures the ferromagnetic
alignment (herding) of the system.

**Module** — A deterministic function from a context to a result. Runs in
one of three phases. May patch axes, contribute a risk multiplier, veto,
or contribute context.

**Phase** — One of PRE_AGOP, POST_AGOP, PRE_LLM. Determines when a module
executes in the pipeline.

**QAOA** — Quantum Approximate Optimisation Algorithm. A variational
algorithm that alternates between a cost Hamiltonian and a mixer
Hamiltonian to approximate the ground state of an optimisation problem.

**Toxic flow** — An order-flow imbalance against the intended action
direction. Forces a flat intent via invariant I4.

**Tunneling probability** — The probability that a quantum state prepared
at the current price level is found strictly beyond a potential barrier
after a short evolution. Patches AGOP's barrier axis in the
`econophysics_tunneling` module.

**Verifier** — The `verify_trade_intent` decorator that enforces invariants
I1 through I9 on every emitted intent.

## Appendix C: References

The Jane Street agent_skills reference: `https://github.com/janestreet/agent_skills`

The AGOP repository: `https://github.com/starwalkerz/AGOP`

The KAIROS repository: `https://github.com/starwalkerz/kairos`

The Causalitybot repository: `https://github.com/starwalkerz/Causalitybot`

The JANUS repository: `https://github.com/starwalkerz/janus`

Belal E. Baaquie, *Quantum Finance: Path Integrals and Hamiltonians for
Options and Interest Rates*. Cambridge University Press, 2004.

Belal E. Baaquie, *Quantum Field Theory for Economics and Finance*.
Cambridge University Press, 2018.

Eisert, Wilkens, and Lewenstein, "Quantum Games and Quantum Strategies",
*Physical Review Letters* 83, 3077 (1999).

Brassard, Høyer, Mosca, and Tapp, "Quantum Amplitude Amplification and
Estimation", *Contemporary Mathematics* 305, 53–74 (2002). The KAIROS
quantum path implements this algorithm.

Farhi, Goldstone, and Gutmann, "A Quantum Approximate Optimization
Algorithm", arXiv:1411.4028 (2014). The herding module implements QAOA
on the Ising cost Hamiltonian.

Kelly, "A New Interpretation of Information Rate", *Bell System Technical
Journal* 35, 917–926 (1956). The risk bound derivation in Section 2.3
follows this paper.

Nash, "Equilibrium Points in N-Person Games", *Proceedings of the National
Academy of Sciences* 36, 48–49 (1950). The AGOP ranking phase consumes
this equilibrium concept.
