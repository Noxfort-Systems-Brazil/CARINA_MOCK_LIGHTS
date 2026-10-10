---
tags: [moc, hub, docs, obsidian, carina, mock, en]
aliases: [Master MOC EN, Knowledge Vault EN]
---

<div align="center">

# CARINA Mock Lights Technical Master Documentation Hub
### Central Index & Simulator Architecture Knowledge Vault
*Noxfort Systems — A State Of Art Company*

</div>

Welcome to the **CARINA Mock Lights** technical documentation library. Designed as a high-fidelity hardware simulator and UTMC2/SNMP testing sandbox, CARINA Mock Lights enables end-to-end integration testing for adaptive traffic light algorithms without requiring physical roadside cabinets.

Compatible with **GitHub** and **[Obsidian](https://obsidian.md/)**.

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
│   ├── CARINA_MOC.md           # Master Documentation Hub (Root)
│   ├── index.md                # MkDocs Entry Point & Portal
│   ├── en/                     # English Documentation Hub (This Directory)
│   └── pt-br/                  # Brazilian Portuguese Documentation Hub
│
└── tests/                      # Automated Test Suite
    ├── test_core.py            # State transition unit tests
    └── test_parser.py          # SUMO network parser unit tests
```

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under Apache 2.0.</small>
</div>
