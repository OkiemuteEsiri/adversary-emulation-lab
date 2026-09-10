from __future__ import annotations

from collections import Counter
from typing import Iterable

from .engine import Finding, score
from .models import Exercise


def render_markdown(exercise: Exercise, findings: Iterable[Finding]) -> str:
    items = tuple(findings)
    counts = Counter(f.severity for f in items)
    lines = [
        f"# Adversary Emulation Validation Report — {exercise.name}",
        "",
        f"**Exercise ID:** `{exercise.exercise_id}`  ",
        f"**Environment:** `{exercise.environment}`  ",
        f"**Owner:** `{exercise.owner}`  ",
        f"**Readiness / Detection Score:** **{score(items)}/100**",
        "",
        "## Summary",
        "",
        f"- Critical: {counts['critical']}",
        f"- High: {counts['high']}",
        f"- Medium: {counts['medium']}",
        f"- Low: {counts['low']}",
        "",
        "## Findings",
        "",
    ]
    if not items:
        lines.append("No control gaps were identified in the supplied synthetic evidence set.")
    for finding in items:
        lines.extend([
            f"### {finding.severity.upper()} — {finding.title}",
            f"- Finding ID: `{finding.finding_id}`",
            f"- ATT&CK / Control: `{finding.technique_id}`",
            f"- Detail: {finding.detail}",
            f"- Remediation: {finding.remediation}",
            "",
        ])
    lines.extend([
        "## Validation Lifecycle",
        "",
        "1. Correct the identified telemetry or detection gap.",
        "2. Re-run the same approved benign scenario in the isolated lab.",
        "3. Capture evidence from every expected telemetry source.",
        "4. Confirm alert fidelity and analyst usability.",
        "5. Record residual risk and close only with reproducible evidence.",
        "",
        "> This report is generated from synthetic lab data and is not evidence of a production compromise.",
    ])
    return "\n".join(lines)
