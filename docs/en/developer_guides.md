---
tags: [developer, guide, setup, cli, snmp, en]
aliases: [Developer Guides EN, Setup Guide EN]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# 🛠️ Developer Guides & Testing Setup

This document provides setup instructions for developers and Net-SNMP CLI debugging workflows.

⬅️ Back to [Master MOC](carina_moc.md) | 🧪 See [Testing](testing.md) | ⚡ See [API Reference](api_reference.md)

---

## 1. Setup Instructions

```bash
# Python backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .[dev,docs]

# Electron frontend
cd ui
npm install
cd ..
```

---

## 2. Execution Commands

- **Full Application (Electron + FastAPI):** `python main.py`
- **Headless Backend:** `python main.py --server`

---

## 3. Net-SNMP CLI Verification

- **Read Description:** `snmpget -v2c -c public 127.0.0.1:1610 1.3.6.1.2.1.1.1.0`
- **Hold Stage 2:** `snmpset -v2c -c public 127.0.0.1:1610 1.3.6.1.4.1.2825.4.2.1.1.4.1.2.1 i 2`
- **Amber Flashing Mode:** `snmpset -v2c -c public 127.0.0.1:1610 1.3.6.1.4.1.2825.4.2.1.1.2.1.255.1 i 1`

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • SPDX-License-Identifier: Apache-2.0</small>
</div>
