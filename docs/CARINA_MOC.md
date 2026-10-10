---
tags: [moc, hub, docs, obsidian, carina, mock, index]
aliases: [CARINA Mock Lights MOC, Master Documentation Hub, Documentation Index, Knowledge Vault]
---

<div align="center">

# CARINA Mock Lights Technical Master Documentation Hub
### Central Index & Simulator Architecture Knowledge Vault
*Noxfort Systems — A State Of Art Company*

</div>

Welcome to the **CARINA Mock Lights** technical documentation library. Designed as a high-fidelity hardware simulator and UTMC2/SNMP testing sandbox, CARINA Mock Lights enables end-to-end integration testing for adaptive traffic light algorithms without requiring physical roadside cabinets.

This master documentation index provides deep technical coverage for core developers, traffic engineers, and test automation specialists. It is fully compatible with both **GitHub** and **[Obsidian](https://obsidian.md/)**.

---

## 🗺️ Codebase Map & Directory Hierarchy

```text
CARINA_MOCK_LIGHTS/
├── main.py                     # Master Orchestrator (CLI flags, Node environment resolver, Electron launcher)
├── ARCHITECTURE.md             # Multi-Tiered System Blueprint & Concurrency Topology
├── pyproject.toml              # Build toolchain & project metadata
├── requirements.txt            # Python runtime dependencies
├── sync.sh                     # Automated Git commit and push workflow
├── mkdocs.yml                  # Material for MkDocs configuration
│
├── core/                       # Core Simulation Engine
│   ├── traffic_light.py        # Single Traffic Light state machine (RED, GREEN, YELLOW, OFF, Observer Pattern)
│   ├── sumo_parser.py          # SUMO .net.xml / .net.xml.gz parser (tlLogic, phases, states)
│   └── manager.py              # TrafficLightManager, Junction lifecycle, controller presets & fault engine
│
├── server/                     # Communication & Protocols Tier
│   ├── api.py                  # FastAPI server, REST routes, WebSocket broadcasting & main_loop sync
│   ├── utmc_server.py          # PySNMP UDP agent runner (port 1610+ per junction)
│   ├── utmc_handlers.py        # OIDHandlerRegistry, stage bitmask decoders (HOLD, FORCE_OFF, OMIT, FLASH)
│   ├── utmc_responders.py      # MockSetCommandResponder & MockGetCommandResponder with VPN firewall
│   ├── utmc_logger.py          # Dedicated connection & command loggers
│   └── utmc_utils.py           # Network IP helpers (get_local_ip)
│
├── ui/                         # Modern Desktop Interface (Electron + React)
│   ├── electron.cjs            # Electron main process (window management, backend child process spawning)
│   ├── index.html              # Vite entrypoint HTML
│   ├── vite.config.ts          # Vite bundler configuration
│   └── src/                    # React 19 Frontend
│       ├── main.tsx            # React application root
│       ├── App.tsx             # Interactive dashboard (Material UI, WebSocket client, controls)
│       └── index.css           # Global typography & layout rules
│
├── docs/                       # Technical Knowledge Vault
│   ├── CARINA_MOC.md           # Master Documentation Hub (This File)
│   ├── index.md                # MkDocs Entry Point & Portal
│   ├── ARCHITECTURE.md         # Internal System Architecture & Mermaid Diagrams
│   ├── API_REFERENCE.md        # FastAPI Endpoints, WebSocket Schemas & SNMP OID Dictionary
│   ├── HARDWARE_SIMULATION.md  # Real-world Controller Presets & Transition State Machines
│   ├── FAULT_INJECTION_ENGINE.md# BER/TLV SNMP Trap Generation & Incident Catalog
│   ├── SUMO_INTEGRATION.md     # Eclipse SUMO Network Ingestion & Phase Extraction
│   ├── UI_AND_DASHBOARD.md     # Electron + React Architecture & Real-Time Sync
│   ├── DEVELOPER_GUIDES.md     # Local Development, CLI Execution & SNMP Debugging
│   ├── TESTING.md              # Pytest Test Suite & Validation Strategy
│   ├── DEPLOYMENT_AND_PACKAGING.md # Electron Packaging & Production Daemon Setup
│   ├── en/                     # English Documentation Hub
│   └── pt-br/                  # Brazilian Portuguese Documentation Hub
│
└── tests/                      # Automated Test Suite
    ├── test_core.py            # State transition unit tests
    └── test_parser.py          # SUMO network parser unit tests
```

---

## ⚡ Module Breakdown

### 1. Simulation Engine (`core/`)
- [`core/traffic_light.py`](../core/traffic_light.py): Implements discrete state transitions (`RED` $\to$ `GREEN` $\to$ `YELLOW` $\to$ `RED`) and notifies observer callbacks.
- [`core/sumo_parser.py`](../core/sumo_parser.py): Robust XML parser extracting topology from SUMO `.net.xml` and `.net.xml.gz`.
- [`core/manager.py`](../core/manager.py): Central manager orchestrating junction threads, Brazilian presets (Dataprom, Siemens, Digicon, Swarco, Kapsch), intergreen timing, and binary SNMP Trap generation.

### 2. Networking & Protocols (`server/`)
- [`server/api.py`](../server/api.py): FastAPI application serving REST endpoints and WebSockets on port `8000`.
- [`server/utmc_server.py`](../server/utmc_server.py): Dedicated PySNMP worker thread per intersection running on port `1610+`.
- [`server/utmc_handlers.py`](../server/utmc_handlers.py): Translates SNMP integer bitmasks to discrete stage requests and vice-versa.
- [`server/utmc_responders.py`](../server/utmc_responders.py): Responds to `GetRequest` and `SetRequest` PDUs, implementing an IP whitelist VPN firewall.

### 3. Graphical Interface (`ui/`)
- [`ui/src/App.tsx`](../ui/src/App.tsx): Material UI dashboard rendering real-time signal heads, junction cards, connection status indicators, and fault injection triggers.
- [`ui/electron.cjs`](../ui/electron.cjs): Electron wrapper orchestrating window lifecycle and managing dev/prod environments.

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under Apache 2.0.</small>
</div>
