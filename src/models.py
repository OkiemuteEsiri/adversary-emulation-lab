from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

VALID_OUTCOMES = {"detected", "not_detected", "not_observed", "not_run"}


@dataclass(frozen=True)
class Technique:
    technique_id: str
    name: str
    tactic: str
    objective: str
    expected_telemetry: Tuple[str, ...]
    approved: bool = True

    def __post_init__(self) -> None:
        if not self.technique_id.startswith("T") or not self.technique_id[1:].replace(".", "").isdigit():
            raise ValueError(f"invalid ATT&CK technique id: {self.technique_id}")
        if not self.expected_telemetry:
            raise ValueError("expected_telemetry must not be empty")


@dataclass(frozen=True)
class Exercise:
    exercise_id: str
    name: str
    environment: str
    owner: str
    authorized: bool
    production: bool
    stop_conditions: Tuple[str, ...]
    techniques: Tuple[Technique, ...]

    def __post_init__(self) -> None:
        if not self.exercise_id.strip():
            raise ValueError("exercise_id is required")
        if not self.owner.strip():
            raise ValueError("owner is required")
        if not self.stop_conditions:
            raise ValueError("at least one stop condition is required")
        if not self.techniques:
            raise ValueError("at least one technique is required")


@dataclass(frozen=True)
class Observation:
    technique_id: str
    telemetry_source: str
    outcome: str
    evidence: str

    def __post_init__(self) -> None:
        if self.outcome not in VALID_OUTCOMES:
            raise ValueError(f"invalid outcome: {self.outcome}")
