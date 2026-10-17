---
tags: [readme, home, carina, mock, lights]
aliases: [CARINA Mock Lights, Root]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->

<div align="center">

# CARINA MOCK LIGHTS
### High-Fidelity Traffic Light Hardware Simulator & UTMC2/SNMP Responder
*Noxfort Systems — A State Of Art Company*

[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat&logo=github)](https://github.com/Noxfort-Systems-Brazil/CARINA)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?style=flat&logo=node.js&logoColor=white)](https://nodejs.org/)
[![React](https://img.shields.io/badge/React-19.2%2B-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Electron](https://img.shields.io/badge/Electron-42.0%2B-47848F?style=flat&logo=electron&logoColor=white)](https://electronjs.org/)
[![SPDX License](https://img.shields.io/badge/SPDX--License--Identifier-Apache--2.0-blue?style=flat)](LICENSE)

---

🌐 **Translations / Idiomas:** **[🇺🇸 English](README.md)** • **[🇧🇷 Português do Brasil](docs/pt-br/README.md)** • **[📚 Documentation Hub](docs/index.md)**

---

</div>

**CARINA Mock Lights** is a realistic traffic signal controller simulator and testing bench designed for the **CARINA** (Controlled Artificial Road-traffic Intelligence Network Architecture) ecosystem. It parses Eclipse SUMO road networks (`.net.xml`), simulates physical signal heads with realistic intergreens, instantiates isolated SNMP responder agents on UDP ports (1610+), dispatches standard UTMC2 traps for hardware and software faults, and provides an interactive desktop dashboard built with **React 19 + TypeScript + Material UI + Electron**.

---

## 📚 Documentation Hub & Knowledge Vault

Explore the full architecture, protocol specifications, and developer guides:

| Card / Subsystem | Focus Area | Direct Link |
| :--- | :--- | :---: |
| 📚 **Master Documentation Hub** | Central Index, Obsidian Vault & Repository Map | [Explore Hub](docs/CARINA_MOC.md) |
| 🏛️ **System Architecture** | Concurrency blueprint, FastApi, PySNMP & Electron | [View Blueprint](ARCHITECTURE.md) |
| ⚡ **API & Protocol Reference** | FastAPI REST endpoints, WebSockets & SNMP OID Table | [View API Specs](docs/API_REFERENCE.md) |
| 🚦 **Hardware Simulation** | Dataprom, Siemens, Digicon, Swarco & Kapsch presets | [View Drivers](docs/HARDWARE_SIMULATION.md) |
| ⚠️ **Fault Injection Engine** | BER/TLV Trap packets, lamp failure & green conflict | [View Faults](docs/FAULT_INJECTION_ENGINE.md) |
| 🗺️ **SUMO Integration** | Network XML parsing, phase mapping & signal groups | [View SUMO Guide](docs/SUMO_INTEGRATION.md) |
| 🖥️ **UI & Electron Dashboard** | React 19, Material UI, Vite & Electron integration | [View UI Guide](docs/UI_AND_DASHBOARD.md) |
| 🛠️ **Developer Guides** | Setup, execution options, snmpwalk & snmpset testing | [View Guides](docs/DEVELOPER_GUIDES.md) |
| 🧪 **Testing & Validation** | Pytest test suite, parser verification & state checks | [View Guidelines](docs/TESTING.md) |
| 🚀 **Deployment & Packaging** | Electron Builder installers & headless production run | [View Deployment](docs/DEPLOYMENT_AND_PACKAGING.md) |

---

## ⚡ Key Highlights

- **SUMO Network Ingestion (`.net.xml` & `.net.xml.gz`):** Instant automatic loading of multi-junction traffic signal geometries and phase logic.
- **Realistic Controller Emulation:** Simulates real-world Brazilian and European controller hardware (Dataprom DP-2000, Siemens ST950, Digicon CD-300, Swarco ITC-3, Dataprom DP-SMART, Kapsch EcoController) with accurate `sysDescr` OID responses.
- **UTMC2 & NTCIP SNMP Responders:** Asynchronous PySNMP daemon running on UDP ports `1610+`, handling discrete stage control (`HOLD`, `FORCE_OFF`, `OMIT`, `EXTEND`, `DEMAND`, `FLASH`, `DARK`).
- **Simulated VPN Firewall:** Security validation restricting SNMP management access strictly to trusted local and VPN subnets.
- **Dynamic Fault Injection:** Generates live hardware and software incidents (LED failure, green conflict, detector drops, RTC drift) via binary SNMP Traps (UDP 162/1620).
- **Modern Desktop Dashboard:** High-performance React 19 interface with real-time WebSocket state streaming, manual stage transition controls, and instant fault trigger buttons.

---

## 🚀 Quick Start

### 1. Requirements
- **Python 3.10+**
- **Node.js 20+** and **npm**

### 2. Installation
```bash
# Set up Python backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set up UI dependencies
cd ui
npm install
cd ..
```

### 3. Running the Simulator

#### Option A: Full Desktop Application (Electron + FastAPI)
```bash
python main.py
```
*Launches both the FastAPI server and the Electron GUI window automatically.*

#### Option B: Headless Backend Server (API & SNMP only)
```bash
python main.py --server
```
*Starts the FastAPI server on `http://0.0.0.0:8000` without opening the graphical window.*

---

<div align="center">
  <img src="docs/assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="48" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • SPDX-License-Identifier: <a href="LICENSE">Apache-2.0</a></small>
</div>
