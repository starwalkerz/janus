```python
"""
Verification tests for the six new physical, energetic, metabolic,
hydrological, thermal, and epidemiological yardstick skills:
  1. solar-bess-adoption
  2. metabolic-burden-yardstick
  3. air-quality-yardstick
  4. drought-monitor
  5. wet-bulb-monitor
  6. unvaccinated-pathogen-monitor
"""

from pathlib import Path
import re
import pytest

from janus.config import Config, load_config

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / "skills"
ROOT_EXAMPLE_CONFIG = ROOT_DIR / "config.example.toml"

NEW_SKILLS = [
    "solar-bess-adoption",
    "metabolic-burden-yardstick",
    "air-quality-yardstick",
    "drought-monitor",
    "wet-bulb-monitor",
    "unvaccinated-pathogen-monitor",
]

REQUIRED_SECTIONS = [
    "## The Readings",
    "## Taxonomy / Decision Matrix",
    "## Secondary Filter",
    "## The Procedure",
    "## The Output Format",
    "## Worked Examples",
    "## Free Data Sources",
    "## Do Not",
    "## Citation Mapping",
]


def _parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    assert match is not None, "Missing or malformed YAML frontmatter"
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


@pytest.mark.parametrize("skill_name", NEW_SKILLS)
def test_skill_file_exists_and_has_valid_frontmatter(skill_name: str) -> None:
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    assert skill_path.exists(), f"Missing skill file: {skill_path}"

    content = skill_path.read_text(encoding="utf-8")
    meta = _parse_frontmatter(content)

    assert meta.get("name") == skill_name
    assert len(meta.get("description", "")) > 25


@pytest.mark.parametrize("skill_name", NEW_SKILLS)
def test_skill_contains_all_required_sections(skill_name: str) -> None:
    content = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert section in content, f"{skill_name} missing required section: {section}"


@pytest.mark.parametrize("skill_name", NEW_SKILLS)
def test_skill_enforces_invariants_and_citation_hygiene(skill_name: str) -> None:
    content = (SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")

    # Invariant I1: Closed action set
    assert "allowed_actions" in content
    assert "FLAT" in content

    # Invariant I5: Downward-only delta authority
    assert "never raise" in content.lower() or "cannot raise" in content.lower()
    assert "1.0" in content and "0.75" in content and "0.25" in content and "0.10" in content

    # Hysteresis halving verification (0.10 -> 0.05)
    assert "0.05" in content

    # Strict citation hygiene when unbound
    assert "skills_cited" in content
    assert "did not bind" in content.lower()

    # 7B-safe prohibition on precise float arithmetic
    assert "precise" in content.lower()


def test_wet_bulb_monitor_exhaustive_hotspots() -> None:
    content = (SKILLS_DIR / "wet-bulb-monitor" / "SKILL.md").read_text(encoding="utf-8")
    required_basins = [
        "persian_gulf",
        "red_sea",
        "indus_valley",
        "ganges_basin",
        "yangtze_valley",
        "nile_valley",
        "gulf_of_mexico",
        "lake_victoria_coast",
        "horn_lowlands",
        "niger_delta",
    ]
    for basin in required_basins:
        assert basin in content, f"wet-bulb-monitor missing critical/major basin: {basin}"
    assert "insidious_surge" in content
    assert "30.0°C" in content


def test_default_config_and_root_toml_include_all_new_skills() -> None:
    default_cfg = Config()
    for skill_name in NEW_SKILLS:
        assert skill_name in default_cfg.active_skills, f"{skill_name} missing from Config().active_skills"

    if ROOT_EXAMPLE_CONFIG.exists():
        loaded_cfg = load_config(ROOT_EXAMPLE_CONFIG)
        for skill_name in NEW_SKILLS:
            assert skill_name in loaded_cfg.active_skills, (
                f"{skill_name} missing from {ROOT_EXAMPLE_CONFIG}"
            )


def test_all_root_toml_files_load_and_reference_existing_skills() -> None:
    for toml_path in ROOT_DIR.glob("config.example*.toml"):
        cfg = load_config(toml_path)
        for skill_name in cfg.active_skills:
            assert (SKILLS_DIR / skill_name / "SKILL.md").exists(), (
                f"{toml_path.name} references missing skill '{skill_name}'"
            )


# ---------------------------------------------------------------------------
# Deterministic Gate Verification (Simulated Evaluation Helper)
# ---------------------------------------------------------------------------

def apply_janus_yardstick_cap(
    agop_ranking: list[str],
    proposed_action: str,
    intended_delta: float,
    state_cap: float,
    persistent: bool,
    skill_name: str,
) -> dict:
    """
    Reference verifier check confirming how any yardstick skill modulates
    (action, delta, skills_cited) under Invariants I1 and I5.
    """
    action = proposed_action if proposed_action in agop_ranking else "FLAT"
    effective_cap = state_cap * 0.5 if persistent else state_cap

    clamped_intended = max(0.0, min(1.0, intended_delta))
    final_delta = min(clamped_intended, effective_cap)

    if action == "FLAT" or final_delta == 0.0:
        action = "FLAT"
        final_delta = 0.0

    bound = final_delta < clamped_intended
    skills_cited = [skill_name] if bound else []

    return {
        "action": action,
        "delta": round(final_delta, 4),
        "skills_cited": skills_cited,
    }


@pytest.mark.parametrize(
    "skill_name,state_cap,persistent,intended,expected_delta,expected_cited",
    [
        ("solar-bess-adoption", 1.0, False, 0.85, 0.85, []),
        ("wet-bulb-monitor", 0.75, False, 0.50, 0.50, []),
        ("air-quality-yardstick", 0.25, False, 0.80, 0.25, ["air-quality-yardstick"]),
        ("drought-monitor", 0.10, False, 0.75, 0.10, ["drought-monitor"]),
        ("wet-bulb-monitor", 0.25, True, 0.75, 0.125, ["wet-bulb-monitor"]),
        ("metabolic-burden-yardstick", 0.10, True, 0.80, 0.05, ["metabolic-burden-yardstick"]),
        ("unvaccinated-pathogen-monitor", 0.10, True, 0.80, 0.05, ["unvaccinated-pathogen-monitor"]),
    ],
)
def test_invariant_i5_and_citation_hygiene_behavior(
    skill_name: str,
    state_cap: float,
    persistent: bool,
    intended: float,
    expected_delta: float,
    expected_cited: list[str],
) -> None:
    verdict = apply_janus_yardstick_cap(
        agop_ranking=["LONG", "FLAT"],
        proposed_action="LONG",
        intended_delta=intended,
        state_cap=state_cap,
        persistent=persistent,
        skill_name=skill_name,
    )
    assert verdict["action"] == "LONG"
    assert verdict["delta"] == expected_delta
    assert verdict["skills_cited"] == expected_cited


def test_invariant_i1_blocks_hallucinated_action() -> None:
    verdict = apply_janus_yardstick_cap(
        agop_ranking=["FLAT"],
        proposed_action="LONG",
        intended_delta=0.80,
        state_cap=1.0,
        persistent=False,
        skill_name="wet-bulb-monitor",
    )
    assert verdict["action"] == "FLAT"
    assert verdict["delta"] == 0.0