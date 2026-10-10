---
tags: [fault, injection, traps, snmp, errors, en]
aliases: [Fault Injection Engine EN, SNMP Traps EN]
---

# ⚠️ Fault Injection Engine & Incident Traps

This document explains the hardware and software failure simulation subsystem in **CARINA Mock Lights** and pure-Python BER/TLV binary SNMP Trap encoding.

⬅️ Back to [Master MOC](carina_moc.md) | 🚦 See [Hardware Simulation](hardware_simulation.md) | ⚡ See [API Reference](api_reference.md)

---

## 1. Error Pool Catalog

### 1.1 Hardware Errors
- **Burnt LED/Lamp (`LAMP_FAILURE`):** OID `1.3.6.1.4.1.2825.4.1.1` - Critical.
- **Green Conflict (`GREEN_CONFLICT`):** OID `1.3.6.1.4.1.2825.4.1.2` - Critical (safety interlock triggered).
- **Detector Failure (`DETECTOR_FAILURE`):** OID `1.3.6.1.4.1.2825.4.1.3` - Warning.
- **Power Degradation (`POWER_ALARM`):** OID `1.3.6.1.4.1.2825.4.1.4` - Warning.
- **Cabinet Door Tamper (`CABINET_DOOR`):** OID `1.3.6.1.4.1.2825.4.1.5` - Warning.

### 1.2 Software Errors
- **Command Rejected (`COMMAND_REJECTED`):** OID `1.3.6.1.4.1.2825.4.2.1` - Warning.
- **Safety Intergreen Violation (`SAFETY_TIME_VIOLATION`):** OID `1.3.6.1.4.1.2825.4.2.2` - Critical.
- **RTC Clock Drift (`RTC_DRIFT`):** OID `1.3.6.1.4.1.2825.4.2.3` - Warning.
- **Local Timetable Error (`PLAN_EXECUTION_ERROR`):** OID `1.3.6.1.4.1.2825.4.2.4` - Warning.
- **Request Queue Overflow (`QUEUE_OVERFLOW`):** OID `1.3.6.1.4.1.2825.4.2.5` - Warning.

---

## 2. BER/TLV Trap Encoding & Transmission

SNMPv2c-Trap datagrams are constructed natively without external dependencies:
- Formatted string payload: `TRAP|<OID>|<LEVEL>|[<CATEGORY>] <NAME>: <MESSAGE>`
- Dispatched via UDP to port **162** (system trap port) and **1620** (user space port) for immediate pickup by CARINA.

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under Apache 2.0.</small>
</div>
