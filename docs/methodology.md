# Methodology

## 1. Authorization and Scope

Every exercise must have an explicit owner, non-production environment, stop conditions, and approved ATT&CK techniques. The execution gate fails closed when any of these controls are violated.

## 2. Threat-Informed Scenario Design

Each scenario maps an ATT&CK technique to a defensive objective and expected telemetry. The project uses benign simulations only; ATT&CK mappings describe the behavior being validated, not instructions for offensive execution.

## 3. Telemetry Expectations

For each technique, define the sources that should observe the scenario, such as identity-provider events, endpoint process telemetry, Windows security events, network flow, and SIEM analytics.

## 4. Detection Validation

Assess whether evidence shows that the behavior was detected, merely observed, not observed, or not run. Missing expected sources and incomplete evidence are separate findings from missing alerts.

## 5. Risk Classification

- **Critical:** authorization/scope gate failure.
- **High:** approved scenario lacks a defensive observation or detection objective is not met.
- **Medium:** expected telemetry source is missing.
- **Low:** evidence reference is incomplete.

## 6. Remediation

Remediation should address the actual defensive gap: sensor coverage, parsing, retention, correlation, detection logic, alert routing, or analyst workflow.

## 7. Retest and Closure

Repeat the same approved benign scenario after remediation, preserve evidence from every expected source, verify alert fidelity, record residual risk, and close only when the result is reproducible.

## Limitations

This is an engineering lab, not a substitute for a full purple-team platform or vendor telemetry. Synthetic data cannot establish that a production control will behave identically under every condition.
