---
tags: [hardware, simulation, controllers, presets, en]
aliases: [Hardware Simulation EN, Controller Presets EN]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# 🚦 Hardware Simulation & Controller Presets

This document specifies physical controller emulation in **CARINA Mock Lights**, including brand presets, transition state machines, intergreen delays, and network protection.

⬅️ Back to [Master MOC](carina_moc.md) | ⚡ See [API Reference](api_reference.md) | ⚠️ See [Fault Injection](fault_injection_engine.md)

---

## 1. Controller Brand Profiles

Intersections inherit realistic manufacturer metadata:
- **Dataprom (DP-2000 / DP-SMART):** Brazilian standard with UTMC2 firmware.
- **Siemens (ST950):** High-capacity international controller.
- **Digicon (CD-300):** Smart controller supporting UTMC2.
- **Swarco (ITC-3):** European high-reliability traffic controller.
- **Kapsch (EcoController):** Adaptive urban mobility controller.

---

## 2. Transition Mechanics & Clearance Safeguards

Direct Green-to-Red switching is prohibited. CARINA Mock Lights enforces:
1. **Target Stage Evaluation:** Incoming stage commands set the target phase index.
2. **Clearance Yellow Phase:** Expiring green links enter yellow clearance while `transition_lock = True`.
3. **Target Stage Locking:** Once clearance timers elapse, target lights turn green and the transition lock releases.

---

## 3. Special Operational Modes

- **ALERT (Flashing Yellow):** All heads flash amber at 1 Hz via OID `.2825.4.2.1.1.2.1.255.1`.
- **OFF (Dark Mode):** Signal heads shut off via OID `.2825.4.2.1.1.2.1.254.1`.

---

## 4. Simulated VPN Firewall

Incoming SNMP packets are checked against trusted private CIDR ranges (`10.0.0.0/8`, `127.0.0.0/8`, `192.168.0.0/16`, `172.16.0.0/12`), safely blocking unverified external internet traffic.

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • SPDX-License-Identifier: Apache-2.0</small>
</div>
