from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import Exercise, Observation, Technique


def load_exercise(path: str | Path) -> Exercise:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {"exercise_id", "name", "environment", "owner", "authorized", "production", "stop_conditions", "techniques"}
    missing = required - raw.keys()
    if missing:
        raise ValueError(f"missing exercise fields: {sorted(missing)}")

    techniques = tuple(
        Technique(
            technique_id=item["technique_id"],
            name=item["name"],
            tactic=item["tactic"],
            objective=item["objective"],
            expected_telemetry=tuple(item["expected_telemetry"]),
            approved=bool(item.get("approved", True)),
        )
        for item in raw["techniques"]
    )
    return Exercise(
        exercise_id=raw["exercise_id"],
        name=raw["name"],
        environment=raw["environment"],
        owner=raw["owner"],
        authorized=bool(raw["authorized"]),
        production=bool(raw["production"]),
        stop_conditions=tuple(raw["stop_conditions"]),
        techniques=techniques,
    )


def load_observations(path: str | Path) -> tuple[Observation, ...]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("observations must be a JSON array")
    return tuple(
        Observation(
            technique_id=item["technique_id"],
            telemetry_source=item["telemetry_source"],
            outcome=item["outcome"],
            evidence=item.get("evidence", ""),
        )
        for item in raw
    )
