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

The stack also includes **STIRPES**, an optional phylogenetic
classification module that groups JANUS solutions by structural type and
commits class and clade hashes to a settlement layer. STIRPES is
unidirectional: it reads from the orchestrator and writes to the chain,
never the reverse. Its output is a queryable public record of what kind
of decision JANUS made, independent of what the decision was.

The stack also includes **opportunity modules**, which invert the
interpretation of KAIROS anomalies and Causalitybot horizons. Where the
standard dampening modules treat these signals as reasons to trade
smaller, the opportunity modules treat them as reasons to trade at all.
The opportunity modules patch AGOP's axes so directional actions rank
higher when a high-conviction, low-downside opportunity qualifies, and
they gate the patch on a downside score so the amplification only fires
when the raw execution environment is safe.

The trading skills and the econophysics skill are custom domain
instructions structured using the SKILL.md specification from:
[https://github.com/janestreet/agent_skills](https://github.com/janestreet/agent_skills)

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
12. Phylogenetic classification (STIRPES)
13. Opportunity modules
14. Running with and without STIRPES
15. License
16. Appendix A: File tree
17. Appendix B: Glossary
18. Appendix C: References

---

## 1. Why the external-ML role is the right slot

A trading system has four functional layers: data, signal, decision, and
execution. The decision layer is where a language model is useful and
where it is dangerous. Useful because it can read a `SKILL.md` body,
weigh a KAIROS anomaly report against a Causalitybot horizon, and
produce a reasoned veto. Dangerous because a model that can size a
position is a model that can lose the account.

JANUS resolves the tension by giving the LLM exactly one authority:
downward. The deterministic risk engine produces an upper bound on
position size; the LLM may reduce it to zero. This is a formal property,
not a policy statement, and the verifier proves it in Section 4.

The LLM is not the trader. The LLM is not the strategist. The LLM is the
analyst sitting between the deterministic risk engine and the execution
layer, with veto power and no sizing authority above the bound. The
deterministic layers do the arithmetic; the language model does the
interpretation; the verifier enforces the boundary between them.

---

## 2. Mathematical specification

### 2.1 The tick

At each tick the pipeline transforms a market snapshot into a trade
intent:

    snapshot → features → PRE_AGOP modules → axes
             → AGOP → POST_AGOP modules → risk bound
             → PRE_LLM modules → LLM → verified intent
             → [optional STIRPES recorder]

The action set is `{LONG, FLAT, SHORT}`. The position size is a fraction
of equity in `[0, position_cap]`, where `position_cap` is the strategy's
absolute ceiling. The pipeline is deterministic given `(snapshot,
configuration, random_seed)` except for the LLM, which is pinned to
temperature zero.

### 2.2 The AGOP decision problem

AGOP ranks a finite set of alternatives under five axes:

    pain, integration, regulatory, readiness, barrier

JANUS constructs the alternatives from the trading action set, populates
the axes from the snapshot, and selects the AGOP mode from the strategy
profile. The axes are computed as follows.

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

**Barrier.** The realised volatility normalised against three times
itself:

    barrier(action) = clip(realized_volatility / (3.0 * realized_volatility), 0.0, 1.0)

which evaluates to one third for every non-flat action. FLAT receives
zero.

The `econophysics_tunneling` module, when enabled, replaces the static
one-third barrier with a physical barrier-penetration probability
computed on a quantum circuit. The opportunity modules (Section 13)
additionally patch the pain, readiness, and barrier axes when a
qualifying opportunity signal is present.

In design-by-contract mode, capacity is derived inside AGOP from the
Weisfeiler–Lehman class cardinality and the Shannon entropies of the two
Nash equilibrium strategies:

    K = max(1, floor(n_wl_classes / (1 + H(σ_DM) * H(σ_CP))))

In legacy mode, capacity is supplied in the theta profile as
`legacy_capacity_override`.

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

The second derivative is strictly negative on the interval `(-1/b, 1)`,
so the stationary point is the unique maximiser. The fraction is clamped
to `[0, 1]` before use. ∎

JANUS computes `p` as the logistic of the signal-to-noise ratio shifted
to `[0.01, 0.99]`, and `b` as the maximum of that ratio and `0.1`. The
Kelly fraction is then multiplied by a strategy-specific coefficient and
combined with the module multiplier.

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

**Legacy mode.** `Theta` carries `K`; `State` carries `gamma`, `Pi`,
`e_1`, `Sigma`, `T`, `D_star`, `convergence_depth`, `nu_star`, `Y_hat`,
`LCB`, `A`, `Phi`, `R`. No formal verification decorator.

**Design-by-contract mode.** `Theta` has no `K`; `State` additionally
carries `K_derived`, `n_wl_classes`, and `certified()`. The
`verifies_theorem_5` decorator enforces

    depth = 1 ∧ ∀v ∈ R : LCB(v) > 0 ∧ nu*(v) = 1 ∧ Phi(v) > 0

A violation raises `AssertionError` before any state escapes.

JANUS's interpretation of a design-by-contract violation is not a crash.
It is the engine telling the bot that no admissible action exists under
the current snapshot. JANUS maps that outcome deterministically to a
flat intent with zero size.

---

## 3. Strategy profiles

Three profiles; every parameter that differs is named.

| Parameter | Conservative | Aggressive | Opportunity |
|---|---|---|---|
| `default_agop_mode` | design-by-contract | legacy | legacy |
| `theta.pain_threshold` | 0.70 | 0.40 | 0.30 |
| `theta.integration_threshold` | 0.70 | 0.50 | 0.40 |
| `theta.regulatory_threshold` | 0.30 | 0.60 | 0.70 |
| `theta.legacy_capacity_override` | 1 | 3 | 5 |
| `lower_confidence_bound_floor` | 0.00 | −0.05 | −0.10 |
| `kelly_coefficient` | 0.25 | 0.60 | 0.80 |
| `position_cap` | 0.10 | 0.35 | 0.30 |
| `toxicity_threshold` | 0.15 | 0.30 | 0.35 |
| `kairos_dampening` | 0.80 | 0.00 | 0.00 |
| `causality_reference_horizon` | 0.60 | 0.30 | 0.25 |
| `causality_gain_coefficient` | 4.0 | 4.0 | 4.0 |
| `llm_confidence_floor` | 0.65 | 0.45 | 0.40 |
| `on_error_default` | fail_closed | fail_open | fail_closed |
| `econophysics_herding_sensitivity` | 0.5 | 0.2 | 0.15 |

The conservative profile is what the design-by-contract AGOP is for: a
contract violation becomes a flat position, the Kelly coefficient is
quarter-Kelly, and the position cap is one tenth of equity. The
aggressive profile accepts the legacy engine's headroom and a looser
lower-confidence-bound floor, and relies on the LLM veto and the
toxic-flow gate for protection. The opportunity profile additionally
assumes that the dampening modules are disabled and the opportunity
modules are enabled (see Section 13.4); its larger position cap (0.30),
higher Kelly coefficient (0.80), and lower LCB floor (−0.10) reflect the
higher-conviction setups the opportunity modules are designed to detect.

---

## 4. Formal invariants

The verifier enforces nine invariants on every emitted intent.

**I1 (closed action set).** The action is in the AGOP ranking or is
FLAT.

    action ∈ ranking(AGOP) ∪ {FLAT}

**I2 (bounded size).** Position size is in the closed interval from zero
to the strategy's position cap.

    0 ≤ position_size ≤ position_cap

**I3 (contract supremacy).** In design-by-contract mode, an AGOP
contract violation forces action FLAT and size zero.

    (agop_mode = DBC ∧ ¬contract_verified) ⟹ (action = FLAT ∧ position_size = 0)

**I4 (toxicity supremacy).** A toxic order-flow imbalance forces FLAT.

    risk_bound.toxic ⟹ (action = FLAT ∧ position_size = 0)

**I5 (downward-only LLM authority).** Position size never exceeds the
risk bound.

    position_size ≤ risk_bound.upper_position_size

**I6 (determinism).** For fixed inputs, configuration, and random seed,
the intent is identical across runs.

**I7 (module monotone composition).** Every module's risk multiplier is
in `[0, 1]`, so the composed bound never exceeds the base cap.

    ∀module ∈ enabled_modules : 0 ≤ module.risk_multiplier ≤ 1
    ⟹ risk_bound.upper_position_size ≤ position_cap

**I8 (module veto supremacy).** Any enabled module that returns a veto
forces FLAT.

    ∃module ∈ enabled_modules : module.veto ⟹ (action = FLAT ∧ position_size = 0)

**I9 (deterministic composition).** Modules execute alphabetically
within each phase.

    ∀phase : modules_by_phase(phase) = sort(modules_by_phase(phase), key = name)

**Theorem.** The verifier is sound with respect to I1 through I9.

**Proof sketch.** I1 through I6 hold by the base verifier. I7 holds
because `validate_result` rejects any risk multiplier outside `[0, 1]`,
and the product of numbers in `[0, 1]` is in `[0, 1]`. I8 holds because
the orchestrator returns FLAT before constructing a non-flat intent when
any module vetoes. I9 holds because `ModuleRegistry.all_by_phase` sorts
alphabetically. Every emitted intent therefore satisfies all nine
invariants; every intent that would violate one is replaced by the flat
intent, which satisfies them vacuously. ∎

The opportunity modules (Section 13) never contribute a risk multiplier;
they only patch axes. Invariant I7 is therefore vacuous for them, and
invariants I5 and I2 still bound the final size.

---

## 5. The module system

A module is a deterministic function from a context to a result. It may
patch axes only in the PRE_AGOP phase, may return a risk multiplier in
`[0, 1]`, may veto from any phase, and may contribute structured context
passed to the LLM.

The ten built-in modules are:

**kairos.** Runs in POST_AGOP. Calls the `starwalkerz/kairos` core via
local import or HTTP. Contributes a risk multiplier equal to
`1 - dampening * amplitude` when the anomaly is flagged, and `1.0`
otherwise. The dampening coefficient is a strategy parameter; the
aggressive and opportunity profiles set it to zero, so a flagged anomaly
does not change sizing for those profiles.

**causality.** Runs in POST_AGOP. Constructs a fresh
`CausalSetMomentumBot`, feeds it the snapshot history as synthetic order
books, and takes the last signal. The horizon proxy is the attractor
strength; the bottleneck proxy is the maximum bottleneck score divided
by ten and capped at one. Contributes a risk multiplier from the
hyperbolic tangent of `(horizon - reference_horizon) *
gain_coefficient`.

**regime.** Runs in PRE_AGOP. Classifies the snapshot into one of three
regimes — calm, normal, choppy — based on the standard deviation of
first differences of the price history. Patches the barrier and
readiness axes accordingly.

**sentiment.** Runs in PRE_AGOP. Reads
`snapshot.external_data["sentiment"]` as a float in `[-1, 1]`. Patches
the pain and readiness axes accordingly. No-op if the key is absent.

**econophysics_tunneling.** Runs in PRE_AGOP. Encodes the nearest
heavy-volume barrier as a potential on a discretized Baaquie
Hamiltonian, evolves the price state through the barrier, and patches
AGOP's `barrier` axis from the resulting tunneling probability. See
Section 11.

**econophysics_herding.** Runs in POST_AGOP. Encodes cross-asset return
correlations as an Ising cost Hamiltonian and runs QAOA to measure the
magnetization order parameter. Contributes a risk multiplier
`1 - sensitivity * |M|`, where `sensitivity` is a strategy parameter.
See Section 11.

**agop_opportunity.** Runs in PRE_AGOP. Uses the raw market opportunity
`Ω_A = |mu|/sigma · (1 - venue_risk) · (1 - slippage/slip_max)`. When
`Ω_A > 0.40` and the downside score `Δ > 0.50`, patches AGOP's axes for
the natural direction (sign of μ). See Section 13.

**causality_opportunity.** Runs in PRE_AGOP. Invokes the actual
`starwalkerz/Causalitybot` via the helpers already used by the
`causality` module, computes `Ω_C = H · β`, and patches AGOP's axes for
the natural direction when `Ω_C > 0.20` and `Δ > 0.50`. See Section 13.

**kairos_opportunity.** Runs in PRE_AGOP. Invokes the actual
`starwalkerz/kairos` via the helpers already used by the `kairos`
module, computes `Ω_K = amplitude`, and patches AGOP's axes for the
natural direction when `Ω_K > 0.05` and `Δ > 0.50`. See Section 13.

**opportunity_synthesizer.** Runs in PRE_LLM. Reads the three PRE_AGOP
opportunity module results from the accumulated prior results and
produces a consensus context for the LLM: `unanimous`, `single`,
`mixed`, or `none`. Never vetoes. See Section 13.

Custom modules are registered by importing a Python path specified in
the configuration's `module_imports` list. The imported module must
export a `module` variable that is a `Module` instance.

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

The econophysics modules run on IQM Resonance when the following
packages are installed and an API token is configured:

```bash
pip install qiskit qiskit-aer iqm-client
```

Without these packages, the modules fall back to exact classical
evolution via `scipy.sparse.linalg.expm_multiply`, which is
mathematically equivalent for the circuit sizes JANUS uses (up to 8
qubits). Installing the quantum packages adds roughly 500 MB to the
environment. The classical fallback produces the same structural
result, with the `backend` field in each module's context set to
`classical-exact` instead of `iqm:*` or `qiskit-aer`.

### 6.4 Optional upstream tools

The AGOP engine, KAIROS anomaly detector, and Causalitybot signal
generator are optional at the dependency level. Each is loaded via
import; if the corresponding directory is not on `PYTHONPATH`, or the
corresponding HTTP endpoint is not configured, the adapter for that tool
returns an unavailable result and the pipeline falls back to AGOP alone.

STIRPES is also optional. Its core (fingerprint extraction, distance
computation, tree construction, clade hashing) requires no additional
packages beyond NumPy and SciPy. Its on-chain settlement layer requires
`web3`:

```bash
pip install web3
```

Without `web3`, the `TezosChainClient` raises `ImportError` on
construction, but the `MockChainClient` works and the rest of STIRPES is
fully functional.

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

The tests cover the verifier invariants, the AGOP bridge, the risk
bound computation, the orchestrator pipeline, the module lifecycle, the
econophysics modules' Hamiltonian symmetry, barrier detection, and risk
multiplier bounds, the STIRPES phylogenetic pipeline, and the
opportunity modules' helpers, individual module behavior, and
synthesizer consensus logic.

---

## 7. Running

### 7.1 Server and web interface

```bash
python run.py
```

The server binds to `http://127.0.0.1:8400` by default. Open that URL in
a browser to access the web interface. The interface exposes a strategy
selector, an AGOP mode selector, a model selector, a module toggle
panel, a market snapshot panel, and a live audit log.

OpenAPI documentation is available at `http://127.0.0.1:8400/docs`.

### 7.2 Command line

Run a single tick:

```bash
python cli.py tick --strategy conservative --agop-mode dbc
```

Disable specific modules for one run:

```bash
python cli.py tick --strategy opportunity --disable kairos causality
```

The CLI prints the full tick record as JSON, identical in structure to
the API response.

### 7.3 Configuration file

Copy `config.example.toml` to `config.toml` and edit it. The
configuration file has the following sections:

- `[strategy]` — the strategy name: `"conservative"`, `"aggressive"`,
  or `"opportunity"`
- `[agop]` — the AGOP mode and the local path or HTTP URL
- `[kairos]` — the KAIROS local path or HTTP URL, and whether to use the
  quantum path
- `[causality]` — the Causalitybot local path or HTTP URL
- `[quantum]` — the IQM token, server, backend, and per-circuit
  parameters for the econophysics modules
- `[stirpes]` — the STIRPES enable flag, chain type, Tezos parameters,
  cipher seed, tree method, flush threshold, and session id
- `[llm]` — the OpenAI-compatible endpoint, model, key, temperature, and
  timeout
- `[skills]` — the SKILL.md directory and the active skill names
- `[risk]` — the equity and the random seed
- `[modules]` — per-module enabled flag and on_error policy, plus the
  list of custom module imports

The recommended configuration for opportunity trading is:

```toml
[strategy]
name = "opportunity"

[modules.kairos]
enabled = false

[modules.causality]
enabled = false

[modules.agop_opportunity]
enabled = true

[modules.causality_opportunity]
enabled = true

[modules.kairos_opportunity]
enabled = true

[modules.opportunity_synthesizer]
enabled = true
```

STIRPES configuration is described in Section 14.

---

## 8. API

The API is served by FastAPI. All endpoints return JSON unless
otherwise noted.

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

STIRPES adds a separate router at `/api/stirpes`. See Section 12.9.

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

For the herding module to consume real cross-asset correlations,
include `external_data["econophysics_assets"]` as a dict mapping asset
name to a list of prices. Without it, the module falls back to a
multi-horizon momentum alignment measure computed from the
single-asset history.

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
    "number_of_weisfeiler_lehman_classes": 3,
    "nash_dm": [0.0, 1.0],
    "nash_cp": [1.0, 0.0]
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
    "contract_forced_flat": false,
    "verdict": "size_clamped"
  },
  "fill": {},
  "modules": {
    "pre_agop": {
      "econophysics_tunneling": {
        "phase": "pre_agop",
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
        }
      },
      "agop_opportunity": {
        "phase": "pre_agop",
        "risk_multiplier": 1.0,
        "veto": false,
        "context": {
          "agop_opportunity": {
            "opportunity": 1.20,
            "direction": "LONG",
            "downside": 0.85,
            "qualified": true
          }
        }
      }
    },
    "post_agop": {
      "econophysics_herding": {
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
        }
      }
    },
    "pre_llm": {
      "opportunity_synthesizer": {
        "phase": "pre_llm",
        "risk_multiplier": 1.0,
        "veto": false,
        "context": {
          "opportunity_synthesis": {
            "consensus": "unanimous",
            "direction": "LONG",
            "confidence": 0.667,
            "contributing_modules": ["agop_opportunity", "kairos_opportunity"]
          }
        }
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

Any field may be omitted; the missing fields retain their current
values.

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

The adapter layer treats AGOP, KAIROS, Causalitybot, the quantum
econophysics modules, and the opportunity modules as opaque
interfaces. Nothing in JANUS assumes their internals; the modules wrap
their public surface.

**Pattern A — AGOP upstream of the pipeline.** The default: AGOP ranks
the trading action set, and JANUS trades the top-ranked action under
the risk bound and the LLM veto.

**Pattern B — KAIROS validates the AGOP window.** If AGOP's ranking is
already suspect (for example, because the axes were constructed from a
snapshot with poor data quality), KAIROS's anomaly flag can dampen the
risk bound before the LLM sees it.

**Pattern C — Causalitybot overrides AGOP.** In the aggressive profile,
the Causalitybot gain can dominate the risk multiplier. When the causal
horizon is strong, the multiplier approaches one. When it is weak, it
approaches zero. The practical effect is that the pipeline trades only
when both AGOP and the causal signal agree.

**Pattern D — Econophysics patches the barrier and shrinks size.** The
tunneling module replaces AGOP's static one-third barrier constant with
a physical tunneling probability computed from the current volume
profile. The herding module shrinks position size when cross-asset
correlations indicate a ferromagnetic consensus. The two effects act in
different phases and cannot collide under the current invariants.

**Pattern E — custom modules plug in without code changes.** A user can
add a module by placing its Python file anywhere on `PYTHONPATH`, adding
the path to the `module_imports` list in `config.toml`, and exporting a
`module` variable from that file. The new module is registered on the
next startup and appears in the web interface's module panel.

**Pattern F — STIRPES classifies and attests without feedback.**
STIRPES reads the orchestrator's `last_agop_result`,
`last_module_contexts`, and `last_intent` after every tick, computes the
fingerprint, and commits the class and clade hashes to a settlement
layer. It never reads from the settlement layer, never feeds the clade
structure back into the orchestrator, and never alters the trade
pipeline. The unidirectionality is proven in Section 12.7.

**Pattern G — Opportunity modules invert signal interpretation.** The
`kairos_opportunity` module (PRE_AGOP) reads the KAIROS report. When
KAIROS flags an anomaly, the module checks whether the anomaly is
aligned with the natural direction (sign of mu) and whether the downside
score is safe. When both conditions hold, it patches AGOP's axes to
favor the natural direction, so the AGOP ranking is more likely to
place the directional action at the top. The other two opportunity
modules do the same for Causalitybot horizons and raw edge. The
`opportunity_synthesizer` (PRE_LLM) reads all three results and
produces structured context indicating whether they agree. The
opportunity modules and the dampening modules are alternatives. The
OPPORTUNITY strategy profile assumes the dampening modules are
disabled.

---

## 10. Limitations

**Paper execution only.** `execution.py` ships a paper broker. A live
broker adapter is out of scope; the interface is documented and the
paper broker can be swapped for a live one by implementing
`PaperBroker.execute`.

**The LLM is audited for authority, not correctness.** The verifier
enforces that the LLM's size does not exceed the risk bound. The
verifier does not enforce that the LLM's rationale is correct, that the
LLM's cited skills are the right ones, or that the LLM's action is
better than the AGOP top-ranked action. A model that produces a
confident wrong rationale is still bounded by the risk bound; a model
that is right but timid will undersize.

**AGOP's axis-construction limitation propagates.** If the axes
constructed from the snapshot are wrong — because `expected_return` is
miscalibrated, because `realized_volatility` is stale, because
`signal_agreement` does not reflect the current signal — the ranking is
wrong. The AGOP README's garbage-in warning applies to JANUS in full.

**KAIROS and Causalitybot are optional.** If either is absent from
`PYTHONPATH` and no HTTP URL is configured, the corresponding module
returns a neutral result and the pipeline runs on AGOP and the
toxic-flow gate alone. The risk multipliers from the absent modules are
set to one, which leaves the bound unchanged.

**The quantum path is optional and off by default in effect.** The
econophysics modules run on IQM Resonance only when
`quantum_iqm_token` is set and the `qiskit` and `iqm-client` packages
are installed. Without those, the modules use Qiskit Aer (when Qiskit
is installed) or exact classical evolution (always available), and
record the backend in the context field.

**The quantum path is slower than the classical fallback.** On the
problem sizes JANUS handles (4 to 8 qubits), the classical exact
fallback is faster than submitting to IQM hardware and produces the
same result. The quantum path matters when the circuit size exceeds the
reach of classical matrix exponentiation (roughly 12 qubits), which is
beyond the current configuration and beyond the coherence budget of
current NISQ hardware. The quantum path is provided for research and
for the theoretical correctness of the algorithm's physical
interpretation, not because it outperforms the classical fallback at
these sizes.

**STIRPES is optional and additive.** STIRPES does not affect the trade
pipeline. Its core requires no additional packages; its on-chain
settlement layer requires `web3`. The `TezosChainClient` is a stub and
must be extended for a real deployment. See Section 12.

**The opportunity modules can amplify a false positive.** If KAIROS
flags an anomaly that is genuinely noise, the opportunity module treats
it as a genuine opportunity and patches the axes accordingly. The
downside gating (`Δ > 0.50`) protects against trading in dangerous
environments but does not protect against trading on a false signal in
a safe environment. Users who run the OPPORTUNITY profile should
monitor the false-positive rate of the underlying signal sources and
tune the qualification thresholds accordingly.

**Not investment advice.** JANUS is research software. It has been
tested against synthetic snapshots and against the reference instances
of the tools it consumes. It has not been tested against live market
data, and its behaviour on adversarial order books is unknown.

**The regime classifier is a proxy.** `regime.py` classifies the market
from the standard deviation of price first differences. This is not a
causal regime classifier; it is a volatility proxy. Real regime
classification requires order book microstructure, which JANUS does not
consume in the reference implementation.

**The sentiment module is a placeholder.** `sentiment.py` reads a
single float from `external_data["sentiment"]`. It does not call any
sentiment provider. A production deployment should replace it with a
module that consumes a real sentiment feed and returns a properly
calibrated signal.

---

## 11. Quantum econophysics modules

JANUS ships two quantum econophysics modules that run on IQM Resonance
when an API token is configured, fall back to Qiskit Aer when Qiskit is
installed but IQM is not, and fall back to exact classical evolution
when neither is available.

### 11.1 Baaquie tunneling

The `econophysics_tunneling` module runs in `PRE_AGOP`. It encodes the
nearest heavy-volume support or resistance level as a potential barrier
on a discretized Baaquie Hamiltonian, evolves the current log-price
state through the barrier for a short evolution window, and measures
the probability of finding the system strictly beyond the barrier.

**Baaquie Hamiltonian.** On a log-price lattice of dimension N = 2^n
with spacing h, the discretized Black–Scholes Hamiltonian is

    H_BS = -(sigma^2 / 2) d^2/dx^2 + (sigma^2 / 2 - r) d/dx + r.

The kinetic term becomes tight-binding hopping
-t_hop * sum_j (|j+1><j| + h.c.). The drift term becomes a small
asymmetric hopping correction. Adding a barrier potential
V(x) = V_0 * exp(-(x - x_B)^2 / (2 w^2)) gives

    H = H_kin + V,
    P_tunnel(t) = ||Pi_out exp(-i H t) |x_0>||^2.

**Theorem (Trotter approximation).** Let U(t) = exp(-i H t) and let
U_S(t, m) = [exp(-i T t/m) exp(-i V t/m)]^m be the first-order
Suzuki–Trotter product. Then

    ||U(t) - U_S(t, m)|| <= (t^2 / (2m)) * ||[T, V]||.

*Proof.* The Baker–Campbell–Hausdorff expansion of
exp(-i T tau) exp(-i V tau) is
exp(-i(T+V)tau - (tau^2/2)[T,V] + O(tau^3)). The leading error per step
is (tau^2/2)[T, V]. Compounding m steps with tau = t/m gives the
stated bound after absorbing higher-order terms. The bound is standard
and is the reason Qiskit's `PauliEvolutionGate` with
`LieTrotter(reps=m)` produces a circuit whose output converges to the
exact evolution as m grows. ∎

**Axis patch.** The module patches AGOP's `barrier` axis. High
tunneling probability means the wall is porous, so the effective
barrier is set low:
`barrier_effective = clip(1 - P_tunnel, 0.05, 0.95)`. The direction of
the barrier (up for resistance, down for support) determines which of
`LONG` or `SHORT` receives the patch; the other side keeps the neutral
0.5. This replaces AGOP's static one-third constant with a genuine
physical barrier-penetration probability.

**Direction selection.** The module computes the nearest barrier above
and the nearest support below the current price from the volume profile
of the snapshot history. It selects the direction whose barrier is
closer in log-price space. If neither exists, the module returns a
neutral result and the pipeline proceeds without the patch.

### 11.2 Ising herding

The `econophysics_herding` module runs in `POST_AGOP`. It encodes the
pairwise return correlation between assets (or, in the single-asset
fallback, between overlapping history windows) as an Ising cost
Hamiltonian, runs QAOA at shallow depth, and measures the magnetization
order parameter M.

**Cost Hamiltonian.**

    H_C = -sum_{i<j} J_ij Z_i Z_j - sum_i h_i Z_i.

J_ij is the clipped Pearson correlation of log-returns between asset i
and asset j. h_i is the hyperbolic tangent of the asset's mean
log-return scaled by 100, which is a momentum drift proxy. The mixer is

    H_M = sum_i X_i.

**Theorem (magnetization as herding measure).** Let

    |psi(beta, gamma)> = prod_{k=1}^p exp(-i beta_k H_M) exp(-i gamma_k H_C) |+>^n

be the QAOA state at depth p. The magnetization

    M(beta, gamma) = (1/n) * sum_i <psi(beta, gamma)| Z_i |psi(beta, gamma)>

satisfies |M| <= 1, with equality if and only if the state is a
computational basis state (fully ferromagnetic) and M = 0 if and only
if the state is uniform over the computational basis (paramagnetic).

*Proof.* Each Z_i has eigenvalues ±1, so |<Z_i>| <= 1 for any state. If
the state is a single basis state |b>, then <Z_i> = ±1 for every i, so
|M| = 1. If the state is uniform, each <Z_i> = 0 by symmetry, so
M = 0. The intermediate values interpolate. ∎

**Risk multiplier.** The module returns 1 - alpha * |M|, with
alpha = 0.5 for the conservative profile, alpha = 0.2 for the
aggressive profile, and alpha = 0.15 for the opportunity profile. In a
herding phase (|M| close to one), position size shrinks; in a
disordered phase (|M| close to zero), position size is unaffected.

**Correlation source.** The module reads
`snapshot.external_data["econophysics_assets"]` when present. The value
must be a dict mapping asset name to a list of prices. When absent, the
module splits the single-asset history into overlapping windows and
computes correlations between windows. The fallback is a multi-horizon
momentum alignment measure, not a cross-asset herding measure; the
module records the distinction in its `notes` field so the LLM can
interpret it correctly.

### 11.3 Backend selection

Each module queries the quantum runner with a preference order:

1. **IQM Resonance** — when `quantum_iqm_token` is set, the circuit is
   transpiled for the requested backend (the provider default if
   `quantum_iqm_backend` is empty) and submitted via
   `backend.run(circuit, shots=N)`.
2. **Qiskit Aer** — when Qiskit is installed but no token is available,
   the same circuit runs on the Aer statevector simulator.
3. **Classical exact** — when Qiskit is not installed, the same
   Hamiltonian is exponentiated via
   `scipy.sparse.linalg.expm_multiply`.

Every path returns the same structural result: a probability vector
for the tunneling circuit, and a `magnetization` plus `cost` for the
QAOA circuit. The `backend` field in each result records which path was
taken, so the audit log preserves provenance.

The classical fallback is exact, not approximate, for both circuits:
the tunneling probability is the exact modulus squared of the evolved
amplitude, and the QAOA magnetization is the exact expectation value
under the optimised (beta, gamma) parameters. The IQM and Aer paths
introduce sampling noise (from shots) and Trotter error (from circuit
depth). The `backend` field distinguishes the three cases so a reader
can tell whether the reported number is exact or sampled.

### 11.4 Two modules, not one

The tunneling effect is a barrier patch, which JANUS permits only in
`PRE_AGOP` (invariant I7). The herding effect is a risk multiplier,
which JANUS permits only in `POST_AGOP` (invariant I9). A single module
cannot legally do both. The two modules share the quantum runner and
the correlation extractor but run in different phases, and each
contributes its effect through the mechanism that the phase permits.
This is the cleanest decomposition consistent with the invariants.

### 11.5 Parameters and their meanings

The two modules expose nine parameters, all with defaults that work on
a four-qubit IQM processor:

| Parameter | Default | Meaning |
|---|---|---|
| `quantum_iqm_token` | `""` | IQM Resonance API token; empty disables IQM path |
| `quantum_iqm_server` | `"https://resonance.iqm.tech"` | IQM Resonance endpoint |
| `quantum_iqm_backend` | `""` | Specific IQM backend; empty uses provider default |
| `quantum_tunneling_qubits` | `4` | Lattice size is 2^n; 4 qubits = 16 price levels |
| `quantum_tunneling_time` | `3.0` | Evolution window in circuit time units |
| `quantum_tunneling_trotter_steps` | `3` | Suzuki–Trotter repetition count |
| `quantum_herding_qubits` | `4` | Number of assets or history windows |
| `quantum_herding_layers` | `1` | QAOA depth |
| `quantum_herding_shots` | `4000` | Shots per QAOA cost evaluation |

The default parameters produce a tunneling circuit of depth
approximately 30 with three Trotter steps, and a QAOA circuit of depth
approximately 10 per layer. Both are well within the coherence budget
of the IQM Garnet processor (20 qubits) at current gate fidelities.

### 11.6 Cost and latency

The tunneling circuit runs once per tick. On IQM Resonance, that is one
quantum job per tick, which is one to four credits depending on backend
availability. On Aer, it is a fraction of a second of CPU. On classical
exact, it is a matrix exponential of dimension 16, which is
sub-millisecond.

The QAOA circuit runs `optimizer_iterations` (default 60) times per
tick for the classical optimisation loop, plus one final evaluation. On
IQM Resonance, that is 61 quantum jobs per tick, which is 61 to 244
credits. **This is prohibitive for live trading on IQM Resonance
without a research budget.** Aer and classical exact complete in
seconds.

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
initial state is a basis state, the evolution is a fixed unitary, and
the shots are reproducible under Aer's seeded simulator. On IQM
hardware the shots are hardware-random, so the reported `P_tunnel` will
vary slightly between runs. To make the full pipeline reproducible
end-to-end, use `quantum_iqm_token = ""` (forcing the Aer path) with
`random_seed = 42`, which is the default.

The QAOA circuit is deterministic under Aer because the COBYLA
optimiser starts from a seeded initial point (`random_seed = 42` in the
runner) and the cost evaluations are seeded. Under IQM hardware, the
shots are hardware-random and the optimiser follows a different
trajectory on different runs.

The `econophysics_tunneling` and `econophysics_herding` modules include
the `backend` field in their context dict, so a downstream auditor can
distinguish a hardware run from an Aer run from a classical run. The
JANUS audit log preserves the context dict per tick.

---

## 12. Phylogenetic classification (STIRPES)

STIRPES is an optional module that groups JANUS solutions by structural
type and commits the groupings to a settlement layer. It does not
affect trading. It reads from the orchestrator, writes to a chain, and
never writes back to the orchestrator. Its purpose is to make the
*shape* of JANUS's decisions externally auditable, queryable, and
comparable across deployments.

### 12.1 What STIRPES does

Every JANUS tick produces a solution. STIRPES extracts a fingerprint
from that solution — a canonical tuple of the AGOP ranking, the
survivor set, the topological classes, the lower-confidence bounds, the
composite scores, the Nash strategies, the module contributions, and
the verifier verdict. It hashes the canonical form into a class
identifier, builds a phylogenetic tree over the accumulated leaf set,
assigns the tick to a clade, and commits the class hash and clade hash
to a settlement layer alongside the tick identifier.

The chain is queryable by either hash. The full solution remains
off-chain, encrypted, and revealed against payment of a token.

### 12.2 The fingerprint

**Definition.** Let `AgopResult` be the normalised AGOP output after
phase 11. Let `module_contexts` be the flattened module contributions
from `Orchestrator.last_module_contexts`. The fingerprint is

    f = (ranking, survivor_set, topology, depth, capacity,
         lower_confidence_bound, composite_score,
         nash_pair, nash_entropy, modules, verdict)

with every floating-point component rounded to six decimals. The
canonical form `κ(f)` is the UTF-8 encoded JSON with sorted keys, no
whitespace, and the pre-rounded values. The class hash is
`SHA256(κ(f))`.

The fingerprint is a deterministic function of `(snapshot,
configuration, random_seed, llm_output, verdict)`. Two ticks with
identical AGOP output, identical module contributions, and identical
verdicts produce identical fingerprints.

### 12.3 The distance

The moduli-space distance between two fingerprints is a weighted sum of
three components:

    d(f, g) = w₁ · D_interleave(f, g)
            + w₂ · D_WL(f, g)
            + w₃ · D_Wasserstein(f, g)

with default weights `w₁ = w₂ = w₃ = 1 / σ`, where `σ` is the sample
standard deviation of each component over the leaf set. The
interleaving component is a bottleneck-style proxy over the
persistence diagrams of the lower-confidence-bound and composite-score
functions. The Weisfeiler–Lehman component is the kernel distance
between the cliff graphs of the topology and survivor-set structures.
The Wasserstein component is the Wasserstein-2 distance on the
module-contribution distributions.

All three components are *approximate* in the sense documented in
`janus/stirpes/distance.py`. They capture the qualitative structure of
the fingerprint space without implementing the full sublevel-set
filtration or the exact optimal-transport computation.

### 12.4 The phylogenetic tree

**Theorem (four-point condition).** A metric space `(L, d)` is
isometrically embeddable into a weighted tree if and only if, for every
four distinct elements `a, b, c, e ∈ L`,

    d(a,b) + d(c,e) ≤ max( d(a,c) + d(b,e),  d(a,e) + d(b,c) )

The proof is due to Buneman (1974). STIRPES uses the Neighbor-Joining
algorithm of Saitou and Nei (1987), whose correctness under bounded
perturbation is due to Atteson (1999):

**Theorem (Atteson bound).** Let `d_true` be a tree-additive metric
with minimum internal edge weight `w_min > 0`. Let `d` be any metric
with `|d(x,y) - d_true(x,y)| < ε` for all pairs. If `ε < w_min / 2`,
the Neighbor-Joining algorithm recovers the topology of the true tree.

The tree is rebuilt over the full leaf set on every flush. The recorder
maintains a persistent leaf set (`_leaf_fingerprints`) capped at
`MAX_LEAF_SET_SIZE = 2000` with FIFO eviction, so tree topology is
stable across batches while memory remains bounded.

### 12.5 Clade hashes and on-chain attestation

For any clade `C ⊆ L`, the clade hash is

    clade_hash(C) = SHA256( ∥_{ℓ ∈ sort(C)} class_hash(ℓ) )

where `∥` denotes concatenation and `sort` is lexicographic ordering of
the 32-byte hashes. The clade hash is invariant to insertion order and
to internal node labels.

The on-chain record per tick is

    TickRecord(
        H_t,                    // SHA256(class_hash ‖ session_id ‖ tick_index ‖ snapshot_hash)
        class_hash,             // bytes32
        historical_clade_hash,  // bytes32
        session_id,             // bytes32
        tick_index,             // uint256
        blocktime,              // uint256
        H_payload               // SHA256(ciphertext)
    )

The `historical_clade_hash` records the clade at the time of commit;
the current clade may differ as the tree evolves. Both are queryable.
The `H_payload` commits to the encrypted fingerprint plus module
contexts; the payload remains off-chain and is revealed against payment
of a token.

The settlement layer is abstracted behind `AbstractChainClient`, with
three implementations: `MockChainClient` (in-memory, for testing),
`TezosChainClient` (stub for Etherlink or a private Tezos rollup;
requires `pip install web3`), and user-extended subclasses for real
deployments. The Solidity contract is `contracts/StirpesRegistry.sol`.

### 12.6 The signal tests

Two phylogenetic signal tests report whether the tree structure is
informative:

**Pagel's λ** is the maximum-likelihood estimate of the parameter in
`V_λ = λ C + (1 - λ) diag(C)`, where `C` is the Brownian-motion
variance-covariance matrix. `λ ≈ 1` indicates strong phylogenetic
signal; `λ ≈ 0` indicates no signal.

**Blomberg's K** is the ratio
`(MSE_observed / MSE_BM) / (MSE_observed / MSE_star)`. `K ≈ 1`
indicates expected signal; `K > 1` indicates conservatism; `K < 1`
indicates convergence or noise.

Both are heuristics, not exact likelihood-ratio tests. The Blomberg's K
approximation uses sample variance rather than the exact BM/star
expected MSE. The signal tests are documented as approximate in
`signal.py`.

### 12.7 Unidirectionality

**Theorem (unidirectionality).** There is no data path in the STIRPES
implementation from the clade structure, the tree, the clade hashes, or
the settlement records back into the JANUS orchestrator, the AGOP
state, or the fingerprint extractor.

**Proof.** The `StirpesRecorder` class has exactly four public methods:
`record(agop_result, module_contexts, snapshot, verdict) -> ClassHash`,
`flush() -> SettlementBatch`, `query_*` methods returning
`list[SettlementRecord]`, and `settle(batch) -> TxHash`. Only `record`
accepts the AGOP output and module contexts, and its return type is
`ClassHash`, which is a `bytes` value with no reference to the inputs.
The remaining methods do not accept the AGOP output and do not return
anything the orchestrator consumes. The module's `__init__.py` does not
import any JANUS module outside `janus.contracts` (which is a primitive
type module), and no JANUS module imports anything from `stirpes`
except `StirpesRecorder` and its return types. The import graph is
therefore acyclic with STIRPES as a sink. ∎

The practical consequence is that JANUS's own development is not driven
by its phylogenetic self-classification. The clade structure is a
record of where the strategy has been, not a prescription for where it
should go. The strategy retains its exploration budget.

### 12.8 Installation and usage

STIRPES requires no additional packages for its core (fingerprint
extraction, distance, tree, clade, signal tests). Its on-chain
settlement layer requires `web3`:

```bash
pip install web3
```

The minimal integration is:

```python
from janus.config import Config
from janus.orchestrator import Orchestrator
from janus.stirpes import StirpesRecorder, MockChainClient, XorCipher

configuration = Config()
orchestrator = Orchestrator(configuration)

chain = MockChainClient(blocktime_seconds=1)
cipher = XorCipher(seed=b"my-stirpes-seed")
recorder = StirpesRecorder(
    chain=chain,
    cipher=cipher,
    tree_method="neighbor_joining",
    flush_threshold=100,
)

# After each tick:
tick_record = orchestrator.tick(snapshot)
recorder.record(
    agop_result=orchestrator.last_agop_result,
    module_contexts=orchestrator.last_module_contexts,
    snapshot=snapshot,
    verdict=tick_record["intent"].get("verdict", "pass"),
)

# Periodically:
batch = recorder.flush()
if batch is not None:
    recorder.settle(batch)
```

The `StirpesRecorder` constructor takes the chain client, the payload
cipher, the tree method, the flush threshold, and the session
identifier. The recorder is not configured through `config.toml`; it is
instantiated with explicit parameters. This is deliberate: STIRPES is a
separate subsystem with its own lifecycle, and its configuration
belongs to its caller, not to the trade pipeline. Section 14 shows how
to build the recorder from `config.toml` via
`bootstrap.build_stirpes_recorder`.

### 12.9 The STIRPES API

STIRPES ships a separate FastAPI router at `/api/stirpes`:

| Method | Path | Description |
|---|---|---|
| POST | `/api/stirpes/flush` | Flush pending ticks and settle. |
| GET | `/api/stirpes/clade/{clade_hash_hex}` | Return tick hashes in a clade. |
| GET | `/api/stirpes/tick/{tick_hash_hex}` | Return settlement record for a tick. |
| GET | `/api/stirpes/session/{session_id}` | Return settlement records for a session. |
| POST | `/api/stirpes/reveal` | Reveal a payload against payment. |

The reveal endpoint is gated by a `RevealGate` backed by a
`TokenLedger`. The ledger is abstract; the deployment wires it to the
actual token contract. The reveal checks the caller's balance or
transfers against the configured thresholds, verifies the ciphertext
hash against the committed `payload_hash`, and returns the decrypted
plaintext.

### 12.10 Dedicated documentation

STIRPES has four dedicated documents in `janus/stirpes/`:

- `README.md` — the formal specification, the theorems, the
  architecture, and the limitations.
- `USAGE.md` — the tutorial: installation, basic flow, recording,
  flushing, querying, signal tests, encryption, integration patterns,
  configuration, testing, troubleshooting.
- `API_REFERENCE.md` — the complete API surface with types, invariants,
  complexity bounds, and every public function, class, and method.
- `TEZOS_CHAIN.md` — the deployment guide: prerequisites, compile and
  deploy steps, contract interface, how to extend the client,
  configuration, gas costs, reorg handling, and limitations.

---

## 13. Opportunity modules

The opportunity modules implement the "opportunity magnifier" pattern:
where the dampening modules treat signal sources as reasons to trade
smaller, the opportunity modules treat them as reasons to trade at all.

### 13.1 Formal definition

**Definition 1 (Opportunity signal).** A signal for direction
`d ∈ {LONG, SHORT}` is a tuple `(d, Ω, Δ)` where `Ω ∈ [0, 1]` is the
opportunity score and `Δ ∈ [0, 1]` is the downside score:

    Δ = (1 - slippage / slippage_maximum) · (1 - venue_risk)

The signal **qualifies** iff `Ω > Ω_min` and `Δ > Δ_min`, with
`Ω_min, Δ_min` being module parameters.

**Definition 2 (Natural direction).** The natural direction is
`d_μ = sign(mu)`. A signal is **aligned** iff `d = d_μ`. Unaligned
signals are discarded.

**Definition 3 (Patches).** For a qualifying aligned signal, the module
patches AGOP's axes for the direction `d`:

    pain[d]      = clip(0.5 + κ_pain · Ω · Δ, 0, 1)
    readiness[d] = clip(0.5 + κ_ready · Ω · Δ, 0, 1)
    barrier[d]   = clip(0.5 - κ_barrier · Ω · Δ, 0, 1)

with `κ_pain, κ_ready, κ_barrier ∈ [0, 0.5]` defaulting to 0.30. The
patches for the opposite direction are left unset, so the base
features' values for that direction survive.

The factor `Ω · Δ` ensures that a strong signal in a dangerous
environment produces only a mild patch.

**Theorem (Bounded magnification).** The modules never produce axis
values outside `[0, 1]`, and the maximum position size is unchanged:
`position_cap × kelly_coefficient × kelly_fraction × 1`. The modules
only shift which action AGOP ranks top; they do not alter the
strategy's cap or the Kelly computation.

**Proof.** Each patch is `clip(·, 0, 1)`. The verifier I1–I9 still
applies. The maximum effective position size is achieved when
`kelly_coefficient × kelly_fraction × module_multiplier = 1`, which is
unchanged by the presence of the opportunity modules. ∎

**Theorem (Downside gating).** A module that requires `Δ > Δ_min`
cannot produce patches when the execution environment is poor (slippage
high or venue_risk high), because the `Δ` factor suppresses the patch
magnitude. In the limit `Δ → 0`, the patches collapse to `0.5`
(neutral), which is the same value AGOP would use in the absence of the
module.

**Proof.** The patches are `0.5 + κ · Ω · Δ` and `0.5 - κ · Ω · Δ`. As
`Δ → 0`, both forms converge to `0.5`. The `clip` operation at
`[0, 1]` is a no-op near `0.5`. Therefore the module has no effect when
downside is infinite. ∎

### 13.2 The four modules

**`agop_opportunity`** (PRE_AGOP) uses the raw market opportunity
`Ω_A = |mu|/sigma · (1 - venue_risk) · (1 - slippage/slip_max)`. It
qualifies when `Ω_A > 0.40` and `Δ > 0.50`. The patch magnitude is
`κ · clip(Ω_A / 2, 0, 1) · Δ`. The `1/2` scaling accounts for the fact
that `Ω_A` can be large (unbounded above) while the opportunity score
should be in `[0, 1]`.

**`causality_opportunity`** (PRE_AGOP) uses the actual
`starwalkerz/Causalitybot` invocation (via the helpers in
`janus/modules/causality.py`) and computes `Ω_C = H · β`, where `H` is
the attractor strength and `β` is the normalized bottleneck score. It
qualifies when `Ω_C > 0.20` and `Δ > 0.50`.

**`kairos_opportunity`** (PRE_AGOP) uses the actual
`starwalkerz/kairos` invocation (via the helpers in
`janus/modules/kairos.py`) and computes `Ω_K = amplitude`. It qualifies
when `Ω_K > 0.05` and `Δ > 0.50`. The anomaly direction is determined
from `recent_slope(history, window_size)`, since KAIROS does not expose
direction in its public report.

**`opportunity_synthesizer`** (PRE_LLM) reads the three PRE_AGOP
results and produces structured context indicating consensus. It never
vetoes. See Section 13.5.

### 13.3 Composition rule

Alphabetically within PRE_AGOP: `agop_opportunity` (a) runs first,
`causality_opportunity` (c) second, `kairos_opportunity` (k) last. The
last module's patch for a given axis wins. This means KAIROS anomalies
have the final say when they qualify, which is correct because cyclical
anomalies are the most reliable of the three signal sources.

### 13.4 Enablement

The opportunity modules are alternatives to the dampening modules. The
recommended configuration is:

```toml
[strategy]
name = "opportunity"

[modules.kairos]
enabled = false

[modules.causality]
enabled = false

[modules.agop_opportunity]
enabled = true

[modules.causality_opportunity]
enabled = true

[modules.kairos_opportunity]
enabled = true

[modules.opportunity_synthesizer]
enabled = true
```

The `OPPORTUNITY` strategy profile sets a larger position cap (0.30), a
higher Kelly coefficient (0.80), a lower LCB floor (−0.10), and looser
thresholds. Combined with the opportunity modules, this produces larger
directional trades when the signals agree, and neutral behavior when
they don't.

### 13.5 The synthesizer

The `opportunity_synthesizer` runs in PRE_LLM. It reads the prior
results (both PRE_AGOP and POST_AGOP) and produces the
`opportunity_synthesis` context:

| Field | Meaning |
|---|---|
| `consensus` | `"unanimous"`, `"single"`, `"mixed"`, `"none"` |
| `direction` | `"LONG"`, `"SHORT"`, or `null` |
| `confidence` | `len(qualifying) / 3` if unanimous; 0.5 if single; 0.0 if mixed/none |
| `contributing_modules` | sorted list of module names that qualified |

The synthesizer never vetoes. It provides context for the LLM.

### 13.6 The `opportunity-analyst` skill

The `opportunity-analyst` skill (in
`skills/opportunity-analyst/SKILL.md`) instructs the LLM how to
interpret the synthesizer's output. When the consensus is unanimous
with confidence ≥ 0.66, the LLM is instructed to return `delta = 1.0`.
When the consensus is single, it returns `delta = 0.5`. When mixed, it
returns `delta = 0.0` (FLAT). The instruction is advisory; the LLM
retains its downward-only authority.

### 13.7 False positives

The opportunity modules can amplify a false positive. The downside
gating (`Δ > 0.50`) protects against trading in dangerous environments
but does not protect against trading on a false signal in a safe
environment. Users who run the OPPORTUNITY profile should monitor the
false-positive rate of the underlying signal sources and tune the
qualification thresholds accordingly.

---

## 14. Running with and without STIRPES

STIRPES is optional. The default configuration has it disabled. The
pipeline runs identically whether the `janus/stirpes/` directory exists
or not, because no core file imports it. When STIRPES is enabled, the
caller constructs a recorder and injects it into the orchestrator; the
orchestrator calls it on every tick and discards its return value.

This section shows the three deployment modes — disabled, enabled with
the mock chain, enabled with a Tezos L2 — and the code that wires each
mode. Nothing else in the configuration changes between modes.

### 14.1 The complete `config.toml` with both subsystems

The configuration surface spans three subsystems: the trading pipeline,
the opportunity modules, and STIRPES. The two `[strategy]` and
`[modules.*]` blocks control the opportunity path; the `[stirpes]`
block controls the STIRPES path. They interact only through the
pipeline: STIRPES reads the verdict that the opportunity (or dampening)
modules produce as part of the tick.

A complete `config.toml` with both subsystems configured:

```toml
[strategy]
name = "opportunity"

[agop]
mode = "legacy"
local_path = "."
http_url = ""

[kairos]
local_path = ""
http_url = ""
quantum = false

[causality]
local_path = ""
http_url = ""

[quantum]
iqm_token = ""
iqm_server = "https://resonance.iqm.tech"
iqm_backend = ""
tunneling_qubits = 4
tunneling_time = 3.0
tunneling_trotter_steps = 3
herding_qubits = 4
herding_layers = 1
herding_shots = 4000

[stirpes]
enabled = false
chain_type = "mock"
tezos_rpc_url = ""
tezos_contract_address = ""
tezos_private_key_env = "STIRPES_PRIVATE_KEY"
cipher_seed = "stirpes-default-seed"
tree_method = "neighbor_joining"
flush_threshold = 100
session_id = "default-session"

[llm]
base_url = "http://localhost:11434/v1"
model = "qwen2.5:7b-instruct"
api_key = "ollama"
temperature = 0.0
timeout_s = 30.0

[skills]
directory = "skills"
active = [
  "toxic-flow-gate",
  "regime-classifier",
  "sizing-discipline",
  "econophysics-analyst",
  "opportunity-analyst",
]

[risk]
equity = 100000.0
seed = 42

[modules]
imports = []

[modules.kairos]
enabled = false
on_error = "fail_open"

[modules.causality]
enabled = false
on_error = "fail_open"

[modules.regime]
enabled = true

[modules.sentiment]
enabled = false

[modules.econophysics_tunneling]
enabled = true
on_error = "fail_open"

[modules.econophysics_herding]
enabled = true
on_error = "fail_open"

[modules.agop_opportunity]
enabled = true
on_error = "fail_open"

[modules.causality_opportunity]
enabled = true
on_error = "fail_open"

[modules.kairos_opportunity]
enabled = true
on_error = "fail_open"

[modules.opportunity_synthesizer]
enabled = true
on_error = "fail_open"
```

This is the default. STIRPES is disabled. The opportunity modules are
enabled under the `opportunity` strategy. The pipeline runs the ten-module
sequence with the opportunity interpretation of the KAIROS and
Causalitybot signals.

### 14.2 Bootstrap code that runs both modes

The caller bootstraps JANUS from the configuration. The same bootstrap
code works for all three STIRPES modes, because
`build_stirpes_recorder` returns `None` when STIRPES is disabled and a
configured recorder when it is enabled:

```python
from janus.bootstrap import (
    build_default_registry,
    build_stirpes_recorder,
)
from janus.config import load_config
from janus.orchestrator import Orchestrator

configuration = load_config("config.toml")
registry = build_default_registry(configuration)
recorder = build_stirpes_recorder(configuration)

orchestrator = Orchestrator(
    configuration,
    registry=registry,
    stirpes_recorder=recorder,
)
```

When `configuration.stirpes_enabled` is `false`, `recorder` is `None`
and the `stirpes_recorder=None` argument behaves identically to not
passing the argument at all. When `configuration.stirpes_enabled` is
`true`, `recorder` is a configured `StirpesRecorder` and the
orchestrator calls `recorder.record(...)` on every tick.

The `build_stirpes_recorder` function imports `janus.stirpes` lazily,
inside the function body. This is what makes STIRPES optional at the
import level: the `from janus.bootstrap import ...` line succeeds
whether the `janus/stirpes/` directory exists or not, because the
import only fires when the function is called with
`stirpes_enabled=True`.

### 14.3 Mode 1 — STIRPES disabled (default)

Configuration:

```toml
[stirpes]
enabled = false
```

Runtime behavior:

- `build_stirpes_recorder` returns `None` without importing
  `janus.stirpes`.
- `Orchestrator.stirpes_recorder` is `None`.
- `tick()` skips the recorder call.
- The four `last_*` attributes (`last_snapshot`, `last_agop_result`,
  `last_intent`, `last_module_contexts`) are still populated, so an
  external consumer can call `recorder.record(...)` on its own if it
  wants.
- The audit log records every tick with the same structure as before
  STIRPES was introduced.

This is the correct mode for production deployments that do not want
on-chain attestation, for research runs that need to be reproducible
without a chain, and for any environment where the `janus/stirpes/`
directory has been removed.

### 14.4 Mode 2 — STIRPES enabled with mock chain

Configuration:

```toml
[stirpes]
enabled = true
chain_type = "mock"
cipher_seed = "test-seed-1"
tree_method = "neighbor_joining"
flush_threshold = 10
session_id = "test-session-1"
```

Runtime behavior:

- `build_stirpes_recorder` imports `janus.stirpes`, constructs a
  `MockChainClient`, an `XorCipher` from `cipher_seed`, and a
  `StirpesRecorder` with `tree_method`, `flush_threshold`, and
  `session_id` from configuration.
- `Orchestrator.stirpes_recorder` is the configured recorder.
- Every `tick()` calls `recorder.record(agop_result,
  module_contexts, snapshot, verdict)` after populating `last_*`.
- Every `flush_threshold` ticks, the recorder auto-flushes: it rebuilds
  the phylogenetic tree over the full leaf set, computes the clade
  hashes, and emits a `SettlementBatch`.
- The caller settles the batch by calling `recorder.settle(batch)`, or
  lets the auto-flush mechanism accumulate batches for periodic
  settlement.

This mode is for testing the STIRPES integration without a chain. The
mock chain stores the settlement records in memory and is fully
queryable via `recorder.query_by_tick`, `recorder.query_by_clade`, and
`recorder.query_by_session`.

Manual settling after run:

```python
batch = recorder.flush()
if batch is not None:
    tx_hash = recorder.settle(batch)
    print(f"Settled {len(batch.tick_hashes)} ticks in tx {tx_hash.hex()}")

# Query by clade:
from janus.stirpes import CladeHash
for clade in set(batch.clade_hashes):
    records = recorder.query_by_clade(CladeHash(clade))
    print(f"Clade {clade.hex()}: {len(records)} ticks")
```

### 14.5 Mode 3 — STIRPES enabled with Tezos L2

Configuration:

```toml
[stirpes]
enabled = true
chain_type = "tezos"
tezos_rpc_url = "https://node.mainnet.etherlink.com"
tezos_contract_address = "0x1234567890abcdef1234567890abcdef12345678"
tezos_private_key_env = "STIRPES_PRIVATE_KEY"
cipher_seed = "production-cipher-seed"
tree_method = "neighbor_joining"
flush_threshold = 50
session_id = "prod-2026-11-14"
```

Runtime behavior:

- `build_stirpes_recorder` imports `janus.stirpes`, reads the private
  key from the environment variable named by `tezos_private_key_env`,
  constructs a `TezosChainClient` with the given `tezos_rpc_url` and
  `tezos_contract_address`, and a `StirpesRecorder` with the configured
  parameters.
- If `tezos_rpc_url` is empty, or `tezos_contract_address` is empty, or
  the environment variable is not set, `build_stirpes_recorder` raises
  `ValueError` before constructing anything. This is a fail-fast
  configuration check, not a runtime failure.
- The recorder is otherwise identical to Mode 2.

**Important caveat.** The `TezosChainClient` in
`janus/stirpes/chain.py` is a stub whose `commit` and `query` methods
raise `NotImplementedError`. Real deployment requires a subclass that
implements `commit` and `query` against the deployed contract ABI, as
shown in `janus/stirpes/TEZOS_CHAIN.md`. The subclass instance must be
constructed by the operator and passed to `StirpesRecorder` directly,
bypassing `build_stirpes_recorder`. This is a code-level substitution,
not a configuration option, because the cipher implementation and the
contract ABI are not values — they are code.

The complete production bootstrap, including the subclass:

```python
import json
from janus.bootstrap import build_default_registry
from janus.config import load_config
from janus.orchestrator import Orchestrator
from janus.stirpes import StirpesRecorder, XorCipher
from janus.stirpes.chain import TezosChainClient
from janus.stirpes.contracts import SessionId


class EtherlinkClient(TezosChainClient):
    """Production subclass that implements commit and query against
    the deployed StirpesRegistry.sol contract."""

    def __init__(self, rpc_url, contract_address, private_key, abi_path):
        super().__init__(rpc_url, contract_address, private_key)
        with open(abi_path) as f:
            self.abi = json.load(f)
        self._contract = self.web3.eth.contract(
            address=contract_address, abi=self.abi,
        )

    def commit(self, batch):
        account = self.web3.eth.account.from_key(self.private_key)
        tx = self._contract.functions.commitBatch(
            list(batch.tick_hashes),
            list(batch.class_hashes),
            list(batch.clade_hashes),
            [s.encode("utf-8") for s in batch.session_ids],
            list(batch.tick_indices),
            list(batch.payload_hashes),
            batch.leaf_set_hash,
            batch.tree_root_hash,
        ).build_transaction({
            "from": account.address,
            "nonce": self.web3.eth.get_transaction_count(account.address),
            "gas": 3_000_000,
            "gasPrice": self.web3.eth.gas_price,
        })
        signed = account.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed.rawTransaction)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.transactionHash

    def query(self, class_hash=None, clade_hash=None, session_id=None, time_range=None):
        from janus.stirpes.contracts import SettlementRecord
        if class_hash is not None:
            tick_hashes = self._contract.functions.getTicksByClass(class_hash).call()
        elif clade_hash is not None:
            tick_hashes = self._contract.functions.getTicksByClade(clade_hash).call()
        elif session_id is not None:
            tick_hashes = self._contract.functions.getTicksBySession(
                session_id.encode("utf-8"),
            ).call()
        else:
            raise ValueError("at least one filter is required")

        records = []
        for tick_hash in tick_hashes:
            tick_record = self._contract.functions.ticks(tick_hash).call()
            record = SettlementRecord(
                tick_hash=tick_record[0],
                class_hash=tick_record[1],
                historical_clade_hash=tick_record[2],
                session_id=tick_record[3].decode("utf-8"),
                tick_index=tick_record[4],
                blocktime=tick_record[5],
                payload_hash=tick_record[6],
            )
            if time_range is not None:
                lo, hi = time_range
                if not (lo <= record.blocktime <= hi):
                    continue
            records.append(record)
        return records


configuration = load_config("config.toml")
registry = build_default_registry(configuration)

import os
chain = EtherlinkClient(
    rpc_url=configuration.stirpes_tezos_rpc_url,
    contract_address=configuration.stirpes_tezos_contract_address,
    private_key=os.environ[configuration.stirpes_tezos_private_key_env],
    abi_path="build/StirpesRegistry.abi",
)
cipher = XorCipher(seed=configuration.stirpes_cipher_seed.encode("utf-8"))
recorder = StirpesRecorder(
    chain=chain,
    cipher=cipher,
    tree_method=configuration.stirpes_tree_method,
    flush_threshold=configuration.stirpes_flush_threshold,
    session_id=SessionId(configuration.stirpes_session_id),
)

orchestrator = Orchestrator(
    configuration,
    registry=registry,
    stirpes_recorder=recorder,
)
```

The distinction between Mode 3 as written here and Mode 3 as
`build_stirpes_recorder` would produce: the built-in builder cannot
construct a subclass it does not know about, so the production
operator writes the subclass once and constructs it directly. The
configuration still drives the parameters, and the orchestrator is
still wired the same way.

### 14.6 The unidirectionality guarantee across all modes

In all three modes, no core file imports `janus.stirpes`. The
orchestrator calls the recorder by structural interface
(`StirpesRecorderProtocol`), discards its return value, and wraps the
call in `try/except` so a recorder failure cannot affect the trade
pipeline. The recorder receives data on every tick but sends nothing
back. The only thing that changes when STIRPES is enabled is that a
settlement record is produced and stored.

Three concrete properties follow:

1. **Deletion safety.** If the `janus/stirpes/` directory is removed,
   the four core files still import cleanly and the pipeline still runs.
   The `build_stirpes_recorder` function would raise `ImportError` only
   if a caller invoked it while `stirpes_enabled=True`, and the four
   `last_*` attributes would simply remain read-only unused defaults.

2. **Failure isolation.** If `recorder.record(...)` raises for any
   reason — an unhandled exception in fingerprint extraction, a chain
   connectivity loss, an encryption failure — the `try/except` in
   `tick()` swallows the exception and the trade pipeline continues
   normally. The tick's audit record is written whether or not the
   recorder succeeded.

3. **The verdict is the only coupling.** The recorder receives the
   intent's `verdict` string (one of `pass`, `size_clamped`,
   `contract_collapse`, `toxicity_collapse`,
   `confidence_floor_collapse`) as part of the fingerprint. The
   verdict is a summary of which branch of `_decide` produced the
   intent, and it is the sole channel by which the trade pipeline's
   outcome influences the STIRPES record. Nothing flows the other
   direction.

This is what "optional" means architecturally: not merely "we can turn
it off in configuration," but "the code that enables it lives in a
separate directory whose absence leaves the rest of the system
unaffected." The three modes above are three ways to exercise the same
architecture. The choice between them is a deployment decision, not a
code change.

### 14.7 Switching between modes at runtime

The `stirpes_enabled` field is read at bootstrap time, not at tick
time. Switching from Mode 1 to Mode 2 or 3 requires rebuilding the
orchestrator:

```python
# Initial deployment: STIRPES disabled
configuration = load_config("config.toml")  # stirpes_enabled = false
orchestrator = Orchestrator(configuration, registry=registry)

# ... trading runs ...

# Enable STIRPES mid-session:
configuration.stirpes_enabled = True
configuration.stirpes_chain_type = "mock"
recorder = build_stirpes_recorder(configuration)
orchestrator = Orchestrator(
    configuration,
    registry=registry,
    stirpes_recorder=recorder,
)
# Trading resumes with STIRPES active from the next tick.
```

The reverse (disabling mid-session) is the same: rebuild the
orchestrator with `stirpes_recorder=None`. The change takes effect on
the next tick, not on the current one.

### 14.8 What is logged in each mode

In Mode 1 (disabled), the audit record for each tick has this shape:

```json
{
  "snapshot": {...},
  "agop": {...},
  "risk": {...},
  "intent": {"verdict": "size_clamped", ...},
  "fill": {...},
  "modules": {...}
}
```

In Modes 2 and 3, the audit record is identical — the STIRPES record is
stored separately, by the recorder, not merged into the orchestrator's
audit log. The orchestrator's audit log is what a JANUS operator
inspects; the STIRPES settlement layer is what an external auditor
inspects. They are distinct surfaces with distinct purposes, and
neither depends on the other.

This is deliberate. The orchestrator's audit log is the record of what
JANUS decided. The STIRPES settlement record is the record of what kind
of decisions JANUS made. The first is internal and mutable; the second
is external and immutable. The separation is what makes the
unidirectionality property observable from outside the system.

---

## 15. License

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
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── registry.py
│   │   ├── kairos.py
│   │   ├── causality.py
│   │   ├── regime.py
│   │   ├── sentiment.py
│   │   ├── quantum_runner.py
│   │   ├── econophysics.py
│   │   ├── opportunity_common.py
│   │   ├── kairos_opportunity.py
│   │   ├── causality_opportunity.py
│   │   ├── agop_opportunity.py
│   │   └── opportunity_synthesizer.py
│   └── stirpes/
│       ├── __init__.py
│       ├── contracts.py
│       ├── fingerprint.py
│       ├── distance.py
│       ├── tree.py
│       ├── clade.py
│       ├── signal.py
│       ├── recorder.py
│       ├── chain.py
│       ├── reveal.py
│       ├── query.py
│       ├── api.py
│       ├── README.md
│       ├── USAGE.md
│       ├── API_REFERENCE.md
│       └── TEZOS_CHAIN.md
├── contracts/
│   └── StirpesRegistry.sol
├── skills/
│   ├── toxic-flow-gate/SKILL.md
│   ├── regime-classifier/SKILL.md
│   ├── sizing-discipline/SKILL.md
│   ├── econophysics-analyst/SKILL.md
│   ├── opportunity-analyst/SKILL.md
│   └── stirpes-analyst/SKILL.md
└── tests/
    ├── test_contracts.py
    ├── test_agop_bridge.py
    ├── test_risk.py
    ├── test_orchestrator.py
    ├── test_modules.py
    ├── test_econophysics.py
    ├── test_opportunity_modules.py
    └── test_stirpes.py
```

## Appendix B: Glossary

**AGOP** — Attributed-Graph Operator Pipeline. A computable decision
engine that composes graph-theoretic, game-theoretic,
systems-theoretic, topological, deductive, stochastic, and
probabilistic operators into a single typed directed acyclic graph. Two
modes: legacy (exogenous capacity) and design-by-contract (endogenous
capacity with verification decorator).

**Baaquie Hamiltonian** — The discretized Black–Scholes Hamiltonian
expressed as a quantum operator on a log-price lattice. Basis for the
tunneling module.

**Causalitybot** — A non-chronological signal generator that identifies
causal horizons and bottlenecks in order flow. Consumed by JANUS via
the `causality` module (dampening) and the `causality_opportunity`
module (magnifier).

**Class hash** — The SHA-256 hash of a fingerprint's canonical form.
Identifies the cell a fingerprint occupies in the stratified solution
space. Stable within the rounding equivalence, differentiable across
cells.

**Clade hash** — The SHA-256 hash of a clade's leaf set. Invariant to
insertion order and internal node labels.

**Contract** — In the design-by-contract AGOP mode, the set of
post-conditions enforced by the `verifies_theorem_5` decorator. In
JANUS, the set of invariants I1 through I9 enforced by the
`verify_trade_intent` decorator.

**Downside score** — `Δ = (1 - slippage/slip_max) · (1 - venue_risk)`.
High Δ means a benign execution environment. Used by the opportunity
modules to gate the amplification patches.

**Econophysics** — The application of physics methods, including
quantum mechanics and statistical mechanics, to economic and financial
systems. The two modules `econophysics_tunneling` and
`econophysics_herding` apply the Baaquie Hamiltonian and the Ising
model respectively.

**Fingerprint** — The canonical tuple of a JANUS solution: the AGOP
ranking, survivor set, topology, depth, capacity, lower-confidence
bounds, composite scores, Nash strategies, module contributions, and
verifier verdict. The input to STIRPES's classification.

**Ising Hamiltonian** — The cost Hamiltonian
`H_C = -sum_{i<j} J_ij Z_i Z_j - sum_i h_i Z_i` used to encode
cross-asset correlations. Basis for the herding module.

**KAIROS** — A cyclical anomaly detector that identifies deviations
from a declared cycle. Consumed by JANUS via the `kairos` module
(dampening) and the `kairos_opportunity` module (magnifier).

**Kelly fraction** — The growth-optimal position fraction for a binary
bet, computed as `f* = p - (1 - p) / b` and clamped to `[0, 1]`.

**LLM** — Large language model. Served over an OpenAI-compatible
endpoint. Consumed by JANUS as the analyst with downward-only sizing
authority.

**Magnetization** — The order parameter `M = (1/n) sum_i <Z_i>` of a
QAOA state on the Ising cost Hamiltonian. Measures the ferromagnetic
alignment (herding) of the system.

**Module** — A deterministic function from a context to a result. Runs
in one of three phases. May patch axes, contribute a risk multiplier,
veto, or contribute context.

**Natural direction** — `d_μ = sign(mu)`. The direction implied by the
expected return. Used by the opportunity modules to filter for aligned
signals.

**Opportunity signal** — A tuple `(d, Ω, Δ)` where `d` is the
direction, `Ω ∈ [0, 1]` is the opportunity score, and `Δ ∈ [0, 1]` is
the downside score. Used by the opportunity modules to decide whether
to patch AGOP's axes.

**Opportunity synthesizer** — A PRE_LLM module that reads the three
PRE_AGOP opportunity module results and produces a consensus context
for the LLM.

**Pagel's λ** — A phylogenetic signal test. `λ ≈ 1` indicates strong
signal; `λ ≈ 0` indicates no signal.

**Phase** — One of PRE_AGOP, POST_AGOP, PRE_LLM. Determines when a
module executes in the pipeline.

**Phylogenetic tree** — A weighted rooted tree over a leaf set, in
which internal nodes represent common ancestors. STIRPES uses
Neighbor-Joining to build the tree over fingerprints.

**QAOA** — Quantum Approximate Optimisation Algorithm. A variational
algorithm that alternates between a cost Hamiltonian and a mixer
Hamiltonian to approximate the ground state of an optimisation problem.

**STIRPES** — The phylogenetic classification and on-chain attestation
module. Reads from the orchestrator, writes to a settlement layer,
never reads back. Its name is the Latin *stirps* (lineage, stock,
family), the philological root of "stirpes" and the taxonomic use of
the word in biology.

**Toxic flow** — An order-flow imbalance against the intended action
direction. Forces a flat intent via invariant I4.

**Tunneling probability** — The probability that a quantum state
prepared at the current price level is found strictly beyond a
potential barrier after a short evolution. Patches AGOP's barrier axis
in the `econophysics_tunneling` module.

**Unidirectionality** — The STIRPES property that no data path exists
from the classification output back into the trade pipeline. Proven in
Section 12.7 and demonstrated operationally in Section 14.6.

**Verdict** — A short string code on every `TradeIntent` that records
how the intent was produced. One of `pass`, `size_clamped`,
`contract_collapse`, `toxicity_collapse`,
`confidence_floor_collapse`. Consumed by STIRPES as part of the
fingerprint.

**Verifier** — The `verify_trade_intent` decorator that enforces
invariants I1 through I9 on every emitted intent.

## Appendix C: References

The Jane Street agent_skills reference:
`https://github.com/janestreet/agent_skills`

The AGOP repository: `https://github.com/starwalkerz/AGOP`

The KAIROS repository: `https://github.com/starwalkerz/kairos`

The Causalitybot repository:
`https://github.com/starwalkerz/Causalitybot`

The JANUS repository: `https://github.com/starwalkerz/janus`

Belal E. Baaquie, *Quantum Finance: Path Integrals and Hamiltonians
for Options and Interest Rates*. Cambridge University Press, 2004.

Belal E. Baaquie, *Quantum Field Theory for Economics and Finance*.
Cambridge University Press, 2018.

Eisert, Wilkens, and Lewenstein, "Quantum Games and Quantum
Strategies", *Physical Review Letters* 83, 3077 (1999).

Brassard, Høyer, Mosca, and Tapp, "Quantum Amplitude Amplification and
Estimation", *Contemporary Mathematics* 305, 53–74 (2002). The KAIROS
quantum path implements this algorithm.

Farhi, Goldstone, and Gutmann, "A Quantum Approximate Optimization
Algorithm", arXiv:1411.4028 (2014). The herding module implements QAOA
on the Ising cost Hamiltonian.

Kelly, "A New Interpretation of Information Rate", *Bell System
Technical Journal* 35, 917–926 (1956). The risk bound derivation in
Section 2.3 follows this paper.

Nash, "Equilibrium Points in N-Person Games", *Proceedings of the
National Academy of Sciences* 36, 48–49 (1950). The AGOP ranking phase
consumes this equilibrium concept.

Buneman, "A Note on the Metric Properties of Trees", *Journal of
Combinatorial Theory, Series B* 17, 48–50 (1974). The four-point
condition in Section 12.4.

Saitou and Nei, "The Neighbor-Joining Method: A New Method for
Reconstructing Phylogenetic Trees", *Molecular Biology and Evolution*
4, 406–425 (1987). The tree-construction algorithm in STIRPES.

Atteson, "The Performance of Neighbor-Joining Methods of Phylogenetic
Reconstruction", *Algorithmica* 25, 251–278 (1999). The correctness
bound in Section 12.4.

Pagel, "Inferring the Historical Patterns of Biological Evolution",
*Nature* 401, 877–884 (1999). The λ signal test in Section 12.6.

Blomberg, Garland, and Ives, "Testing for Phylogenetic Signal in
Comparative Data: Behavioral Traits Are More Labile", *Evolution* 57,
717–745 (2003). The K signal test in Section 12.6.
