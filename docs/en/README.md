---
tags: [readme, home, carina, mock, en]
aliases: [English Documentation Hub, Overview EN]
---

<div align="center">

# CARINA MOCK LIGHTS
### High-Fidelity Traffic Light Simulator & UTMC2/SNMP Responder
*Noxfort Systems — A State Of Art Company*

[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat&logo=github)](https://github.com/Noxfort-Systems-Brazil/CARINA)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?style=flat&logo=node.js&logoColor=white)](https://nodejs.org/)
[![React](https://img.shields.io/badge/React-19.2%2B-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Electron](https://img.shields.io/badge/Electron-42.0%2B-47848F?style=flat&logo=electron&logoColor=white)](https://electronjs.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat)](../../LICENSE)

---

🌐 **Translations / Idiomas:** **[🇺🇸 English](README.md)** • **[🇧🇷 Português do Brasil](../pt-br/README.md)** • **[📚 Main Portal](../index.md)**

---

</div>

**CARINA Mock Lights** is a high-fidelity traffic signal controller simulator and testing bench designed for the **CARINA** ecosystem. It parses Eclipse SUMO road networks (`.net.xml`), simulates physical signal heads with realistic intergreens, instantiates isolated SNMP responder agents on UDP ports (1610+), dispatches standard UTMC2 traps for hardware/software faults, and provides an interactive desktop dashboard built with **React 19 + TypeScript + Material UI + Electron**.

---

## 📚 Technical Modules

| Card / Subsystem | Focus Area | Direct Link |
| :--- | :--- | :---: |
| 📚 **Master MOC** | Central Index, Obsidian Vault & Repository Map | [Explore Hub](carina_moc.md) |
| 🏛️ **System Architecture** | Concurrency blueprint, FastApi, PySNMP & Electron | [View Blueprint](architecture.md) |
| ⚡ **API & Protocol Reference** | FastAPI REST endpoints, WebSockets & SNMP OID Table | [View API Specs](api_reference.md) |
| 🚦 **Hardware Simulation** | Dataprom, Siemens, Digicon, Swarco & Kapsch presets | [View Simulation](hardware_simulation.md) |
| ⚠️ **Fault Injection Engine** | BER/TLV Trap packets, lamp failure & green conflict | [View Faults](fault_injection_engine.md) |
| 🗺️ **SUMO Integration** | Network XML parsing, phase mapping & signal groups | [View SUMO Guide](sumo_integration.md) |
| 🖥️ **UI & Electron Dashboard** | React 19, Material UI, Vite & Electron integration | [View UI Guide](ui_and_dashboard.md) |
| 🛠️ **Developer Guides** | Setup, execution options, snmpwalk & snmpset testing | [View Guides](developer_guides.md) |
| 🧪 **Testing & Validation** | Pytest test suite, parser verification & state checks | [View Guidelines](testing.md) |
| 🚀 **Deployment & Packaging** | Electron Builder installers & headless production run | [View Deployment](deployment_and_packaging.md) |

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under Apache 2.0.</small>
</div>
