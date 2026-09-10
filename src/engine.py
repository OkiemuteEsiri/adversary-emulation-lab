from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable

from .models import Exercise, Observation


@dataclass(frozen=True)
class Finding:
    finding_id: str
    severity: str
    title: str
    technique_id: str
    detail: str
    remediation: str


def _id(exercise_id: str, technique_id: str, title: str) -> str:
    raw = f"{exercise_id}|{technique_id}|{title}".encode("utf-8")
    return sha256(raw).hexdigest()[:12]


def execution_gate(exercise: Exercise) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    if not exercise.authorized:
        reasons.append("exercise is not explicitly authorized")
    if exercise.production:
        reasons.append("production execution is prohibited by this lab")
    blocked = [t.technique_id for t in exercise.techniques if not t.approved]
    if blocked:
        reasons.append(f"unapproved techniques present: {', '.join(blocked)}")
    return (not reasons, tuple(reasons))


def assess(exercise: Exercise, observations: Iterable[Observation]) -> tuple[Finding, ...]:
    observed = list(observations)
    findings: list[Finding] = []
    allowed, gate_reasons = execution_gate(exercise)
    if not allowed:
        for reason in gate_reasons:
            title = "Exercise execution gate blocked"
            findings.append(Finding(_id(exercise.exercise_id, "GATE", reason), "critical", title, "GATE", reason, "Correct scope/authorization before any exercise activity."))
        return tuple(findings)

    for technique in exercise.techniques:
        matches = [o for o in observed if o.technique_id == technique.technique_id]
        if not matches:
            title = "No defensive observation recorded"
            findings.append(Finding(_id(exercise.exercise_id, technique.technique_id, title), "high", title, technique.technique_id, "No observation was supplied for the approved scenario.", "Run the approved benign simulation in the isolated lab and capture telemetry evidence."))
            continue
        outcomes = {m.outcome for m in matches}
        sources = {m.telemetry_source for m in matches}
        missing_sources = set(technique.expected_telemetry) - sources
        if "detected" not in outcomes:
            title = "Detection objective not met"
            findings.append(Finding(_id(exercise.exercise_id, technique.technique_id, title), "high", title, technique.technique_id, f"Observed outcomes: {sorted(outcomes)}", "Create or tune detection logic, validate ingestion, then retest the same scenario."))
        if missing_sources:
            title = "Expected telemetry source missing"
            findings.append(Finding(_id(exercise.exercise_id, technique.technique_id, title), "medium", title, technique.technique_id, f"Missing: {sorted(missing_sources)}", "Validate sensor coverage, parsing, retention, and query accessibility."))
        if any(not m.evidence.strip() for m in matches):
            title = "Observation evidence incomplete"
            findings.append(Finding(_id(exercise.exercise_id, technique.technique_id, title), "low", title, technique.technique_id, "At least one observation lacks an evidence reference.", "Attach a synthetic event ID, query result, or report reference to every observation."))
    return tuple(findings)


def score(findings: Iterable[Finding]) -> int:
    weights = {"critical": 35, "high": 20, "medium": 10, "low": 3}
    penalty = sum(weights[f.severity] for f in findings)
    return max(0, 100 - min(100, penalty))
