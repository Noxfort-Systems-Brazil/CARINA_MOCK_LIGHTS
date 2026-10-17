---
tags: [sumo, parser, xml, tllogic, en]
aliases: [SUMO Integration EN, Network Ingestion EN]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# 🗺️ SUMO Network Ingestion & Phase Extraction

This document explains how **CARINA Mock Lights** ingests and parses road network geometries and traffic signal configurations from **Eclipse SUMO**.

⬅️ Back to [Master MOC](carina_moc.md) | 🏛️ See [Architecture](architecture.md) | 🚦 See [Hardware Simulation](hardware_simulation.md)

---

## 1. Gzip Transparency

Supports plain XML `.net.xml` and compressed `.net.xml.gz` files seamlessly, streaming decompressed bytes via standard library `gzip`.

---

## 2. Ingestion of `<tlLogic>`

The parser locates all `<tlLogic>` nodes:
- Extraction of phase dwell duration (`duration`) in integer seconds.
- Extraction of light characters (`state`): `g`/`G` (Green), `y`/`Y` (Yellow), `r`/`R` (Red), `u` (Amber flash), `s`/`O` (Off).
- Discrete indexing of every phase as a UTMC2 stage bitmask ($2^k$).

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • SPDX-License-Identifier: Apache-2.0</small>
</div>
