"""
skills.py — loader for Jane Street SKILL.md folders.

The format is a directory containing SKILL.md with YAML frontmatter followed
by a Markdown body.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    body: str
    path: Path


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    metadata = yaml.safe_load(parts[1]) or {}
    return metadata, parts[2].lstrip("\n")


def load_skill(directory: Path) -> Skill:
    markdown_path = directory / "SKILL.md"
    if not markdown_path.exists():
        raise FileNotFoundError(f"no SKILL.md in {directory}")
    metadata, body = _split_frontmatter(
        markdown_path.read_text(encoding="utf-8")
    )
    return Skill(
        name=metadata.get("name", directory.name),
        description=metadata.get("description", ""),
        body=body,
        path=markdown_path,
    )


def load_skills(root: str | Path, names: Iterable[str]) -> list[Skill]:
    root_path = Path(root)
    output: list[Skill] = []
    for name in names:
        directory = root_path / name
        if directory.is_dir():
            output.append(load_skill(directory))
    return output


def compose_system_prompt(skills: list[Skill]) -> str:
    if not skills:
        return "You are a disciplined trading analyst. Reply with JSON only."
    blocks = [
        "You are a disciplined trading analyst operating under the following",
        "skills. Cite a skill by name when it drives your decision.",
        "",
    ]
    for skill in skills:
        blocks.append(f"## Skill: {skill.name}")
        blocks.append(f"_{skill.description}_")
        blocks.append("")
        blocks.append(skill.body.strip())
        blocks.append("")
    blocks.append(
        "Reply with a single JSON object: "
        '{"action": "LONG|FLAT|SHORT", "delta": 0.0-1.0, '
        '"confidence": 0.0-1.0, "rationale": "...", "skills_cited": ["..."]}'
    )
    return "\n".join(blocks)