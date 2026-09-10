# Architecture

## Purpose

This repository models adversary emulation as a controlled security-engineering workflow rather than an exploitation toolkit. The design separates scenario definition, authorization, evidence collection, assessment, and reporting.

## Components

1. **Domain models (`src/models.py`)** validate exercises, ATT&CK techniques, stop conditions, expected telemetry, and observations.
2. **Ingestion (`src/io.py`)** loads JSON using fail-closed field validation.
3. **Control engine (`src/engine.py`)** applies an execution gate before evaluating detection coverage.
4. **Reporting (`src/report.py`)** converts findings into an executive/technical Markdown report.
5. **CLI (`src/cli.py`)** provides reproducible offline execution suitable for CI.
6. **Synthetic data (`data/`)** represents isolated-lab exercises and defensive evidence only.

## Security Boundaries

The project intentionally does not implement exploitation, credential theft, persistence, evasion, malware delivery, C2, or real-target interaction. Production execution is explicitly blocked by the engine.

## Data Flow

`exercise.json + observations.json -> validation -> execution gate -> ATT&CK-by-ATT&CK telemetry analysis -> findings -> score -> Markdown report`

## Design Properties

- deterministic finding identifiers;
- immutable domain objects;
- explicit authorization and production-scope gates;
- reproducible synthetic evidence;
- separation of telemetry visibility from alert detection;
- remediation and retest lifecycle suitable for purple-team engineering.
