---
tags: [api, reference, rest, websocket, snmp, utmc2, oids]
aliases: [API Reference, REST API, WebSocket API, SNMP OID Table]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# ⚡ API & Protocol Reference

This document provides the complete technical specification for all communication interfaces in **CARINA Mock Lights**, including the FastAPI REST API, WebSocket real-time event streaming, and the UTMC2/NTCIP SNMP OID registry.

⬅️ Back to [Documentation Hub](CARINA_MOC.md) | 🏛️ See [System Architecture](ARCHITECTURE.md) | 🚦 See [Hardware Simulation](HARDWARE_SIMULATION.md)

---

## 1. FastAPI REST API (`http://localhost:8000`)

### 1.1 Ingest SUMO Network
Loads and instantiates junctions from an Eclipse SUMO network file.

- **Endpoint:** `POST /api/load`
- **Request Body:**
  ```json
  {
    "file_path": "/absolute/path/to/network.net.xml"
  }
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "message": "Network loaded successfully."
  }
  ```

---

### 1.2 List Active Junctions
Returns telemetry and current signal head status for all initialized junctions.

- **Endpoint:** `GET /api/junctions`
- **Response:**
  ```json
  {
    "junctions": [
      {
        "id": "J1",
        "utmc_port": 1610,
        "utmc_address": "192.168.1.50:1610",
        "brand": "Dataprom",
        "model": "DP-2000",
        "lights": [
          {"id": 0, "state": "GREEN", "label": "Link 0"},
          {"id": 1, "state": "RED", "label": "Link 1"}
        ],
        "failure": false,
        "disable_fixed_plans": false,
        "connected": true,
        "protocol": "UTMC2"
      }
    ]
  }
  ```

---

### 1.3 Toggle Connection Failure Mode
Simulates hardware communication failure (agent drops incoming SNMP requests).

- **Endpoint:** `POST /api/junctions/{junction_id}/failure`
- **Request Body:**
  ```json
  {
    "state": true
  }
  ```
- **Response:**
  ```json
  {
    "status": "success"
  }
  ```

---

### 1.4 Toggle Fixed Plan Disabling
Disables autonomous fixed-time cycle progression, allowing full remote override control.

- **Endpoint:** `POST /api/junctions/{junction_id}/fixed-plans`
- **Request Body:**
  ```json
  {
    "state": true
  }
  ```
- **Response:**
  ```json
  {
    "status": "success"
  }
  ```

---

### 1.5 Simulate Hardware or Software Fault
Injects a randomized or targeted alarm and emits an asynchronous SNMP Trap packet to UDP port 162/1620.

- **Endpoint:** `POST /api/junctions/{junction_id}/simulate-error`
- **Request Body:**
  ```json
  {
    "category": "HARDWARE"
  }
  ```
  *(Supported categories: `"HARDWARE"`, `"SOFTWARE"`)*
- **Response:**
  ```json
  {
    "status": "success",
    "error_info": {
      "category": "HARDWARE",
      "type": "GREEN_CONFLICT",
      "level": "CRITICAL",
      "oid": "1.3.6.1.4.1.2825.4.1.2",
      "name": "Conflito de Verdes",
      "message": "Intervenção da placa de segurança: Conflito de fases verdes detectado"
    }
  }
  ```

---

## 2. WebSocket Real-Time Streaming (`ws://localhost:8000/ws`)

Subscribing clients receive instant state push notifications whenever a signal head or junction connection status mutates.

### 2.1 State Change Frame
Emitted when a signal group changes color (`RED`, `GREEN`, `YELLOW`, `OFF`):
```json
{
  "type": "state_change",
  "junction_id": "J1",
  "light_id": 0,
  "state": "GREEN"
}
```

### 2.2 Status Change Frame
Emitted when a junction connection or heartbeat status transitions:
```json
{
  "type": "status_change",
  "junction_id": "J1",
  "connected": true
}
```

---

## 3. UTMC2 / SNMP OID Reference Table

The PySNMP agent listens on UDP port `1610 + (port - 8080)` per intersection and processes the following OIDs:

| Function | ASN.1 OID Pattern | Type | Operation | Description |
| :--- | :--- | :---: | :---: | :--- |
| **System Description** | `1.3.6.1.2.1.1.1.0` | `OCTET STRING` | `GET` | Emulated controller brand, model and firmware |
| **Stage Hold** | `.2825.4.2.1.1.4.1.2.1` | `INTEGER` | `SET` | Stage bitmask to hold active ($1 \ll \text{stage}$) |
| **Force Off** | `.2825.4.2.1.1.4.1.3.1` | `INTEGER` | `SET` | Forces current stage termination to clearance |
| **Stage Omit** | `.2825.4.2.1.1.4.1.7.1` | `INTEGER` | `SET` | Omits stage from rotation sequence |
| **Green Extension** | `.2825.4.2.1.1.4.1.6.1` | `INTEGER` | `SET` | Extends phase green window |
| **Stage Demand** | `.2825.4.2.1.1.4.1.5.1` | `INTEGER` | `SET / GET` | Demand bitmask (returns 255 to prompt AI) |
| **Amber Flash** | `.2825.4.2.1.1.2.1.255.1` | `INTEGER` | `SET` | Overrides intersection to Flashing Yellow (`ALERT`) |
| **Dark Mode** | `.2825.4.2.1.1.2.1.254.1` | `INTEGER` | `SET` | Shuts down lamps to Dark Mode (`OFF`) |
| **Active Stage** | `.2825.4.2.1.1.4.1.4.1` | `INTEGER` | `GET` | Bitmask of stage currently displaying Green |
| **Leaving Stage** | `.2825.4.2.1.1.4.1.8.1` | `INTEGER` | `GET` | Bitmask of stage transitioning through Yellow |
| **Pedestrian Demand** | `.2825.4.2.1.1.4.1.9.1` | `INTEGER` | `GET` | Pedestrian call detection bitmask |

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • SPDX-License-Identifier: Apache-2.0</small>
</div>
