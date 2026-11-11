"""
llm.py — OpenAI-compatible client for the external-ML role.

Any endpoint serving /v1/chat/completions works. Temperature is pinned to
0.0 for determinism.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Optional

import httpx

from janus.contracts import Action


@dataclass(frozen=True)
class LLMDecision:
    action: Action
    delta: float
    confidence: float
    rationale: str
    skills_cited: list[str]
    raw: str = ""


def _parse_json_object(text: str) -> Optional[dict]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None


def _coerce(obj: dict) -> LLMDecision:
    try:
        action = Action(str(obj.get("action", "FLAT")).upper())
    except ValueError:
        action = Action.FLAT
    delta = float(obj.get("delta", 0.0))
    confidence = float(obj.get("confidence", 0.0))
    rationale = str(obj.get("rationale", ""))[:2000]
    cited = [str(item) for item in obj.get("skills_cited", [])][:10]
    return LLMDecision(
        action=action,
        delta=max(0.0, min(1.0, delta)),
        confidence=max(0.0, min(1.0, confidence)),
        rationale=rationale,
        skills_cited=cited,
    )


class LLMClient:
    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: str = "ollama",
        temperature: float = 0.0,
        timeout_seconds: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.timeout_seconds = timeout_seconds

    def decide(
        self, system_prompt: str, user_payload: dict
    ) -> LLMDecision:
        body = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": json.dumps(user_payload, default=str),
                },
            ],
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    json=body,
                    headers=headers,
                )
                response.raise_for_status()
                data = response.json()
            content = data["choices"][0]["message"]["content"]
        except Exception as exception:
            return LLMDecision(
                action=Action.FLAT,
                delta=0.0,
                confidence=0.0,
                rationale=f"llm error: {type(exception).__name__}",
                skills_cited=[],
            )

        obj = _parse_json_object(content)
        if obj is None:
            return LLMDecision(
                action=Action.FLAT,
                delta=0.0,
                confidence=0.0,
                rationale="llm returned non-JSON",
                skills_cited=[],
                raw=content[:500],
            )
        decision = _coerce(obj)
        return LLMDecision(
            action=decision.action,
            delta=decision.delta,
            confidence=decision.confidence,
            rationale=decision.rationale,
            skills_cited=decision.skills_cited,
            raw=content[:500],
        )