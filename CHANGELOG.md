# Changelog

All notable changes to **CARINA Mock Lights** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-10

### Added
- **Modern React 19 + Material UI Desktop UI**: Interactive desktop interface packaged with Electron 42 and Vite, providing visual traffic light signal status, junction switcher, and real-time control buttons.
- **Hardware & Software Fault Injection Subsystem**: Ability to trigger realistic field alarms via SNMP Traps (UDP 162 / 1620) using BER/TLV encoded packets:
  - Hardware: Lamp/LED failure, Green-on-Green conflict, Detector failure, Power alarm, Cabinet door open.
  - Software: Command rejected by firmware, Safety intergreen violation, RTC clock drift, Local plan execution error, Request queue overflow.
- **Brazilian Controller Presets**: Autodetection and assignment of real controller brands (Dataprom DP-2000 / DP-SMART, Siemens ST950, Digicon CD-300, Swarco ITC-3, Kapsch EcoController) with accurate `sysDescr` OID responses.
- **Transition State Machine & Clearance Timings**: Intermediate yellow/clearance states when executing remote stage transitions (`HOLD`, `FORCE_OFF`) to emulate real cabinet intergreens.
- **FastAPI Backend & WebSockets**: Real-time state broadcasting via `/ws` and REST API endpoints (`/api/load`, `/api/junctions`, `/api/junctions/{id}/failure`, `/api/junctions/{id}/fixed-plans`, `/api/junctions/{id}/simulate-error`).
- **Comprehensive Documentation Suite**: Replicated CARINA_CORE standard with Material for MkDocs, Obsidian-compatible Master MOC, and bilingual hubs (English and Português do Brasil).

---

## [1.0.0] - 2026-08-10

### Added
- **SUMO Network Parser (`sumo_parser.py`)**: Extractor for SUMO `.net.xml` and `.net.xml.gz` network files, mapping `tlLogic`, phase durations, and signal link strings.
- **Traffic Light State Engine (`traffic_light.py` & `manager.py`)**: Multi-threaded junction manager orchestrating concurrent intersection state machines.
- **UTMC2 SNMP Responder (`server/utmc_server.py`)**: Asynchronous PySNMP engine responding to standard UTMC2 OID commands (`HOLD`, `FORCE_OFF`, `OMIT`, `EXTEND`, `DEMAND`, `FLASH`, `DARK`).
- **Activity & Connection Logging**: Dedicated event loggers recording raw packet connections and SUMO state conversions to disk.
- **Initial Test Suite**: Unit tests verifying state machine transitions and basic XML parsing.
