<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->

# Security Policy

## Supported Versions

CARINA Mock Lights is under active development. Only the latest release on `main` receives official security updates.

| Version | Supported          |
| ------- | ------------------ |
| v1.1.x  | :white_check_mark: |
| v1.0.x  | :white_check_mark: |
| < 1.0   | :x:                |

## Security Considerations

**CARINA Mock Lights** simulates field traffic signal hardware and operates local UDP SNMP responder sockets (port 1610+) as well as HTTP/WebSocket servers (port 8000).

- **Simulated VPN Firewall**: The SNMP command responders feature built-in private IP validation (`10.x.x.x`, `127.x.x.x`, `192.168.x.x`, `172.x.x.x`), blocking unverified external requests.
- **Isolation**: When connected to live networks, ensure the simulator runs in a contained, sandbox environment without public UDP exposure.

## Reporting a Vulnerability

If you discover a security vulnerability, please do **NOT** open a public issue on GitHub.
Report it directly to:

**security@noxfort.com** *(Noxfort Systems Security Team)*

We will review your submission within 48 hours and provide remediation updates.
