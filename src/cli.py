from __future__ import annotations

import argparse
from pathlib import Path

from .engine import assess, execution_gate, score
from .io import load_exercise, load_observations
from .report import render_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate authorized adversary-emulation detection evidence")
    parser.add_argument("exercise")
    parser.add_argument("observations")
    parser.add_argument("--report", default="reports/latest.md")
    args = parser.parse_args()

    exercise = load_exercise(args.exercise)
    allowed, reasons = execution_gate(exercise)
    if not allowed:
        print("EXECUTION GATE: BLOCKED")
        for reason in reasons:
            print(f"- {reason}")
    observations = load_observations(args.observations)
    findings = assess(exercise, observations)
    output = render_markdown(exercise, findings)
    destination = Path(args.report)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(output, encoding="utf-8")
    print(f"score={score(findings)} findings={len(findings)} report={destination}")
    return 0 if not any(f.severity == "critical" for f in findings) else 2


if __name__ == "__main__":
    raise SystemExit(main())
