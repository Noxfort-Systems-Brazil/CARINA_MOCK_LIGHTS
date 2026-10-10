---
tags: [sumo, network, parser, tllogic, xml, traffic, lights]
aliases: [SUMO Integration, Network Parser, SUMO .net.xml]
---

# 🗺️ SUMO Network Ingestion & Phase Extraction

This document explains how **CARINA Mock Lights** parses and interprets road networks created with **Eclipse SUMO** (Simulation of Urban MObility).

⬅️ Back to [Documentation Hub](CARINA_MOC.md) | 🏛️ See [System Architecture](ARCHITECTURE.md) | 🚦 See [Hardware Simulation](HARDWARE_SIMULATION.md)

---

## 1. File Formats & Gzip Transparency

CARINA Mock Lights natively supports both standard XML text networks (`.net.xml`) and compressed gzip archives (`.net.xml.gz`):

```python
if file_path.endswith('.gz'):
    with gzip.open(file_path, 'rb') as f:
        tree = ET.parse(f)
else:
    tree = ET.parse(file_path)
```

This prevents developers from having to manually uncompress large metropolitan SUMO road networks prior to loading them into the simulator.

---

## 2. Traffic Light Logic Schema (`<tlLogic>`)

SUMO network files define intersection signal timings within `<tlLogic>` tags. The parser scans the XML DOM for all `<tlLogic>` elements:

```xml
<tlLogic id="cluster_25749444_25749445" type="static" programID="0" offset="0">
    <phase duration="31" state="GGgrrrGGgrrr"/>
    <phase duration="4"  state="yygrrryygrrr"/>
    <phase duration="6"  state="rrGrrrrrGrrr"/>
    <phase duration="31" state="rrrGGgrrrGGg"/>
    <phase duration="4"  state="rrryygrrryyg"/>
    <phase duration="6"  state="rrrrrGrrrrrG"/>
</tlLogic>
```

### 2.1 Extracted Data Models
- **`PhaseData`:**
  - `duration`: Phase dwell duration in integer seconds.
  - `state`: String representing individual signal head states for each connection lane.
- **`JunctionData`:**
  - `id`: Junction unique string identifier.
  - `phases`: Chronological list of `PhaseData` cycles.
  - `num_lights`: Total count of independent signal heads ($N = \text{len}(\text{state})$).

---

## 3. Signal Character Mapping

Signal characters from SUMO phase states are translated dynamically to the core `LightState` enum:

| SUMO Character | Meaning | Mapped `LightState` | Visual Display |
| :---: | :--- | :---: | :---: |
| `g`, `G` | Priority Green / Green Right-of-Way | `GREEN` | 🟢 Bright Green |
| `y`, `Y` | Yellow / Amber Warning | `YELLOW` | 🟡 Amber Warning |
| `r`, `R` | Red / Stop | `RED` | 🔴 Stop Red |
| `u`, `o` | Flashing Yellow / Transitional | `YELLOW` | 🟡 Caution Amber |
| `s`, `O` | Off / Dark | `OFF` | ⚫ Unlit |

---

## 4. Discrete Stage Indexing for UTMC2

In the UTMC2 protocol, stages are indexed as discrete integer powers of 2 (bitmasks):
$$\text{Stage Mask} = 2^k \quad \text{where } k \in [0, M-1]$$

Each parsed SUMO phase is mapped directly to a green stage index, allowing CARINA's reinforcement learning agents to request specific SUMO phase states through standard UTMC2 `HOLD` and `FORCE_OFF` OID bitmasks.

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under Apache 2.0.</small>
</div>
