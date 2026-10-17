---
tags: [fault, injection, traps, snmp, errors, ber, tlv, hardware, software]
aliases: [Fault Injection Engine, Error Simulation, SNMP Traps]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# ⚠️ Fault Injection Engine & Incident Traps

This document explains the hardware and software failure simulation subsystem in **CARINA Mock Lights**. It covers error definitions, BER/TLV binary packet encoding, and asynchronous SNMP Trap dispatching to CARINA's incident listeners.

⬅️ Back to [Documentation Hub](CARINA_MOC.md) | 🚦 See [Hardware Simulation](HARDWARE_SIMULATION.md) | ⚡ See [API & Protocols](API_REFERENCE.md)

---

## 1. Failure Categories & Error Pool

CARINA Mock Lights contains an incident catalog divided into **HARDWARE** and **SOFTWARE** faults:

### 1.1 Hardware Failures (`HARDWARE_ERRORS_POOL`)

| Type | Level | OID | Name | Description |
| :--- | :---: | :--- | :--- | :--- |
| `LAMP_FAILURE` | `CRITICAL` | `1.3.6.1.4.1.2825.4.1.1` | Falha de Lâmpada/LED | Burnt red LED or bulb failure on signal group 2 |
| `GREEN_CONFLICT`| `CRITICAL` | `1.3.6.1.4.1.2825.4.1.2` | Conflito de Verdes | Hardware conflict board intervention: Green conflict detected |
| `DETECTOR_FAILURE`| `WARNING` | `1.3.6.1.4.1.2825.4.1.3` | Falha de Sensor/Laço | Inductive loop presence detector cut or signal drop |
| `POWER_ALARM` | `WARNING` | `1.3.6.1.4.1.2825.4.1.4` | Alerta de Energia | External power grid fluctuation, operating on UPS battery |
| `CABINET_DOOR` | `WARNING` | `1.3.6.1.4.1.2825.4.1.5` | Alerta de Armário Aberto | Cabinet door tampering or open switch triggered |

### 1.2 Software Failures (`SOFTWARE_ERRORS_POOL`)

| Type | Level | OID | Name | Description |
| :--- | :---: | :--- | :--- | :--- |
| `COMMAND_REJECTED` | `WARNING` | `1.3.6.1.4.1.2825.4.2.1` | Comando Rejeitado | Firmware rejects requested transition due to sequence conflict |
| `SAFETY_TIME_VIOLATION` | `CRITICAL` | `1.3.6.1.4.1.2825.4.2.2` | Violação de Tempo | Request denied due to active intergreen safety clearance |
| `RTC_DRIFT` | `WARNING` | `1.3.6.1.4.1.2825.4.2.3` | Desincronização de Relógio | Internal Real-Time Clock out of sync with central NTP |
| `PLAN_EXECUTION_ERROR` | `WARNING` | `1.3.6.1.4.1.2825.4.2.4` | Erro de Plano Local | Failure in local timetable matrix schedule switch |
| `QUEUE_OVERFLOW` | `WARNING` | `1.3.6.1.4.1.2825.4.2.5` | Estouro de Fila | SNMP request queue temporarily overwhelmed |

---

## 2. Low-Level SNMP Trap Packet Construction (BER/TLV)

Rather than depending on heavy external binaries, CARINA Mock Lights generates native **Basic Encoding Rules (BER)** Type-Length-Value (TLV) encoded SNMPv2-Trap UDP datagrams in pure Python:

```python
def pack_tlv(tag: int, value: bytes) -> bytes:
    length = len(value)
    if length < 128:
        len_bytes = bytes([length])
    else:
        len_bytes = bytes([0x81, length])
    return bytes([tag]) + len_bytes + value
```

### 2.1 Packet Structure
1. **VarBind Object Identifier:** Standard enterprise trap OID sequence (`1.3.6.1.4.1.2825.4.1`).
2. **Payload Value (`OCTET STRING`):**
   ```text
   TRAP|<OID>|<LEVEL>|[<CATEGORY>] <NAME>: <MESSAGE>
   ```
3. **PDU Assembly:**
   - Tag `0x30`: SEQUENCE (VarBind)
   - Tag `0xa7`: SNMPv2-Trap-PDU (RequestID, ErrorStatus, ErrorIndex, VarBindList)
   - Tag `0x30`: Top-level Message Sequence (Version=v2c, Community=public, PDU)

---

## 3. Dispatch & Receiver Targeting

When triggered (via the desktop GUI or `POST /api/junctions/{id}/simulate-error`), the engine broadcasts the UDP datagram to target ports:

```python
ports_to_send = [trap_port] if trap_port != 162 else [162, 1620]
for p in ports_to_send:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(snmp_msg, (target_ip, p))
    sock.close()
```

- **Port 162:** Standard IANA SNMP Trap port (monitored by operating system daemons and CARINA's native Go Hardware Gateway).
- **Port 1620:** Non-privileged user-space testing port (allowing execution without root privileges).

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • SPDX-License-Identifier: Apache-2.0</small>
</div>
