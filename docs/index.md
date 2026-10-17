---
tags: [home, index, carina, mock, hub]
aliases: [Documentation Index, Overview, Portal]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


<div align="center">

# CARINA Mock Lights Documentation Hub
### Technical Master Portal & Architecture Index
*Noxfort Systems — A State Of Art Company*

</div>

Welcome to the technical documentation library for **CARINA Mock Lights** — an enterprise-grade traffic light hardware simulation engine and UTMC2/SNMP testing bench designed for the **CARINA** ecosystem.

Designed to operate seamlessly on **GitHub** and as an **[Obsidian](https://obsidian.md/) Knowledge Vault**, this documentation suite covers SUMO network ingestion, hardware controller emulation, SNMP command responders, fault injection protocols, and the modern desktop interface.

---

## 🗺️ Master Navigation & Modules

| Subsystem / Dimension | Focus Area | Direct Link |
| :--- | :--- | :---: |
| 📚 **Master Map of Content** | Primary Obsidian Hub & Codebase Directory Map | [Explore Hub](CARINA_MOC.md) |
| 🏛️ **System Architecture** | Concurrency Topology, FastApi, PySNMP & Electron Engine | [View Blueprint](ARCHITECTURE.md) |
| ⚡ **API & Protocol Reference** | FastAPI REST Endpoints, WebSocket Protocol & OID Table | [View API Specs](API_REFERENCE.md) |
| 🚦 **Hardware Simulation** | Controller Brand Presets, Intergreen States & Transitions | [View Simulation](HARDWARE_SIMULATION.md) |
| ⚠️ **Fault Injection Engine** | BER/TLV Trap Packets, Hardware/Software Error Catalog | [View Faults](FAULT_INJECTION_ENGINE.md) |
| 🗺️ **SUMO Integration** | Parsing `.net.xml`, Phase Sequences & Signal Groups | [View SUMO Guide](SUMO_INTEGRATION.md) |
| 🖥️ **UI & Electron Dashboard** | React 19, Material UI, Vite & Electron Integration | [View UI Guide](UI_AND_DASHBOARD.md) |
| 🛠️ **Developer Guides** | Setup, Execution Modes, snmpwalk & snmpset Testing | [View Guides](DEVELOPER_GUIDES.md) |
| 🧪 **Testing & Validation** | Pytest Test Suite, Parser Checks & State Assertions | [View Guidelines](TESTING.md) |
| 🚀 **Deployment & Packaging** | Electron Builder Installers & Standalone Production Daemon | [View Deployment](DEPLOYMENT_AND_PACKAGING.md) |

---

## ⚡ Architecture Topology

```text
       ┌────────────────────────────────────────────────────────┐
       │               CARINA MOCK LIGHTS ENGINE                │
       │           (FastAPI + PySNMP + Electron React)          │
       └──────────────────────────┬─────────────────────────────┘
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      ▼                           ▼                           ▼
┌──────────────┐          ┌──────────────┐          ┌──────────────────┐
│FastAPI Server│          │Junction Thread│         │  Electron React  │
│(HTTP / WS)   │ ◄──────► │(State Engine)│ ◄──────► │ (Dashboard UI)   │
└──────┬───────┘          └──────┬───────┘          └──────────────────┘
       │                         │
       ▼                         ▼
┌──────────────┐          ┌──────────────┐
│  PySNMP Agent│          │  SNMP Traps  │
│ (UDP 1610+)  │          │ (UDP 162/1620│
└──────────────┘          └──────────────┘
```

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • SPDX-License-Identifier: Apache-2.0</small>
</div>
