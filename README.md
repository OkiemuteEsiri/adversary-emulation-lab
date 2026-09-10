# Adversary Emulation Lab

A recruiter-facing purple-team engineering project for designing and validating **authorized, threat-informed adversary-emulation exercises** against synthetic lab environments. The project focuses on authorization gates, MITRE ATT&CK scenario design, expected telemetry, detection outcomes, remediation, and evidence-based retesting—not exploit delivery.

## Problem Statement

Security teams often document ATT&CK techniques without proving whether telemetry and detections actually cover the behaviors they care about. This lab models a repeatable workflow that turns ATT&CK-mapped scenarios into measurable defensive validation results while enforcing strict scope and safety controls.

## Architecture

```text
exercise.json + observations.json
            |
            v
      validated models
            |
            v
      execution gate
   authorization / scope
            |
            v
 ATT&CK telemetry analysis
            |
            v
 findings + 0-100 score
            |
            v
   Markdown validation report
```

Core modules:

- `src/models.py` — immutable exercise, technique, and observation models.
- `src/io.py` — fail-closed JSON ingestion.
- `src/engine.py` — authorization gate, coverage assessment, deterministic findings, scoring.
- `src/report.py` — executive/technical Markdown output.
- `src/cli.py` — reproducible offline workflow.
- `data/` — realistic synthetic exercise and evidence datasets.
- `tests/` — unit tests covering safety gates and detection-validation logic.
- `docs/` — architecture and methodology documentation.
- `reports/` — example recruiter-facing validation output.

## Safety and Execution Controls

The engine blocks evaluation as an executable exercise when any of the following is true:

- explicit authorization is absent;
- the target environment is marked production;
- an ATT&CK scenario is not approved.

This repository contains no credential theft, persistence tooling, C2, malware, defense impairment, exploit payloads, production targeting, or real client data.

## MITRE ATT&CK Scenario Mapping

| Technique | Scenario | Defensive objective |
|---|---|---|
| T1078 — Valid Accounts | Synthetic anomalous identity context | Validate identity-provider and SIEM detection evidence |
| T1059.001 — PowerShell | Harmless local PowerShell process activity | Validate endpoint process telemetry and SIEM analytics |
| T1021.001 — RDP | Synthetic RDP logon between isolated lab hosts | Validate Windows Security, network-flow, and SIEM coverage |

ATT&CK mappings describe defensive validation objectives only and are not instructions for offensive execution.

## Risk Classification

| Severity | Meaning |
|---|---|
| Critical | Authorization or scope gate failure |
| High | No observation or detection objective not met |
| Medium | Expected telemetry source missing |
| Low | Observation evidence incomplete |

The bounded 0–100 score deducts weighted penalties from the exercise posture so reviewers can compare validation runs consistently.

## Usage

Requires Python 3.11+ and no third-party runtime dependencies.

```bash
python -m src.cli data/exercise.json data/observations.json --report reports/latest.md
python -m unittest discover -s tests -v
```

The CLI writes a Markdown report and returns a non-zero exit code when a critical authorization/scope condition exists.

## Example Validation Flow

1. Define an approved isolated-lab scenario and explicit stop conditions.
2. Map each scenario to ATT&CK and expected telemetry sources.
3. Run only a benign authorized simulation outside this repository.
4. Record defensive evidence in `observations.json`.
5. Evaluate detection outcomes and missing telemetry.
6. Remediate logging, parsing, correlation, detection, or analyst-workflow gaps.
7. Repeat the same approved scenario and close only with reproducible evidence.

## Tests

The test suite covers:

- authorized non-production execution;
- unauthorized exercise blocking;
- production-scope blocking;
- unapproved-technique blocking;
- missing observations;
- missing detections;
- missing telemetry sources;
- incomplete evidence;
- deterministic finding IDs;
- bounded scoring.

## CI/CD Security Checks

`.github/workflows/ci.yml` uses read-only repository permissions and performs:

- Python compilation;
- unit-test discovery;
- validation of the synthetic exercise dataset;
- generation of a CI validation report.

## Design Decisions

- **Fail closed:** ambiguous authorization and malformed input should stop validation rather than be silently accepted.
- **Deterministic evidence:** stable finding IDs improve remediation tracking and retest comparison.
- **Telemetry ≠ detection:** a source can observe activity without producing an actionable alert; the model treats these separately.
- **Synthetic by default:** all included identities, hosts, event IDs, and evidence references are fictional.
- **Defensive focus:** ATT&CK is used to structure detection validation, not to operationalize offensive tradecraft.

## Remediation and Validation

A finding is not considered resolved just because a rule or sensor was changed. Closure requires repeating the same approved benign scenario, proving expected telemetry is available, verifying alert fidelity and analyst usability, and recording residual risk.

See `docs/methodology.md` for the complete lifecycle and `reports/example-report.md` for a sample output.

## Skills Demonstrated

- Purple-team and adversary-emulation program design
- MITRE ATT&CK mapping
- Detection engineering validation
- Security telemetry architecture
- Risk classification and scoring
- Python security automation
- Defensive evidence handling
- Remediation and retest governance
- Unit testing and CI/CD controls
- Executive and technical security reporting

## Limitations

This lab does not interact with EDR, SIEM, identity, or network platforms directly. Synthetic observations are useful for engineering and portfolio demonstration but do not prove production-control effectiveness. Real validation requires authorized environment-specific telemetry and change-management processes.

## Roadmap

- Add schema versioning and richer input validation.
- Add ATT&CK tactic-level coverage summaries.
- Add detection-quality dimensions such as precision, latency, and analyst actionability.
- Add safe adapters for exported SIEM/EDR evidence rather than live credentials.
- Add historical retest comparison and control-regression reporting.
- Add machine-readable JSON reporting alongside Markdown.
