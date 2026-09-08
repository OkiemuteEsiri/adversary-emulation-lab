# Detection Telemetry Matrix

| ATT&CK Area | Example Lab Activity | Primary Telemetry | Validation Question |
|---|---|---|---|
| Initial Access | Controlled phishing simulation or exposed service test | Email gateway, proxy, EDR | Was the attempt blocked or alerted? |
| Execution | Approved command execution in lab | EDR, PowerShell, Sysmon | Was process ancestry and command line captured? |
| Credential Access | Synthetic credential-access test | EDR, Windows Security, identity logs | Did the control detect suspicious access? |
| Discovery | Host/domain discovery in lab | EDR, Sysmon, network telemetry | Was reconnaissance visible? |
| Lateral Movement | Approved remote administration path | Windows Security, EDR, firewall | Was movement correlated across hosts? |
| Persistence | Benign persistence simulation | EDR, registry/service logs | Did monitoring detect the configuration change? |
| Command & Control | Benign beacon-like lab traffic | DNS, proxy, firewall, NDR | Was periodic anomalous traffic identifiable? |
| Exfiltration | Synthetic test-data transfer | Proxy, DLP, firewall | Was unusual egress detected and contained? |

Use this matrix before each exercise to define expected visibility and after the exercise to record detection coverage and gaps.
