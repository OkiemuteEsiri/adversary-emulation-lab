# Adversary Emulation Validation Report — Synthetic Identity and Endpoint Detection Validation

**Exercise ID:** `AE-2026-001`  
**Environment:** `isolated-lab`  
**Owner:** `Purple Team Lab`  
**Readiness / Detection Score:** **90/100**

## Summary

- Critical: 0
- High: 0
- Medium: 1
- Low: 0

## Findings

### MEDIUM — Expected telemetry source missing
- Finding ID: `example-network-flow-gap`
- ATT&CK / Control: `T1021.001`
- Detail: Expected `network-flow` evidence was not supplied for the synthetic RDP validation scenario.
- Remediation: Validate network-flow sensor coverage and ingestion, then repeat the same isolated-lab scenario and attach evidence.

## Positive Coverage

- T1078 synthetic identity scenario observed and detected by identity and SIEM controls.
- T1059.001 benign PowerShell activity observed by endpoint telemetry; SIEM evidence exists but detection logic should be reviewed where outcome differs.
- T1021.001 synthetic RDP activity observed by Windows Security and SIEM data.

## Validation Lifecycle

1. Correct the telemetry gap.
2. Re-run the approved benign scenario in the isolated lab.
3. Capture network-flow evidence alongside Windows and SIEM evidence.
4. Confirm fidelity and analyst usability.
5. Record residual risk and close only with reproducible evidence.

> All identifiers and events in this example are synthetic.
