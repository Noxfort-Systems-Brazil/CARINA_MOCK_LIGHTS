---
tags: [api, reference, rest, websocket, snmp, utmc2, en]
aliases: [API Reference EN, Endpoints EN, OID Table EN]
---

# ⚡ API & Protocol Reference

This document provides the complete technical specification for all communication interfaces in **CARINA Mock Lights**: FastAPI REST API, WebSocket real-time event streaming, and UTMC2/NTCIP SNMP OID registry.

⬅️ Back to [Master MOC](carina_moc.md) | 🏛️ See [Architecture](architecture.md) | 🚦 See [Hardware Simulation](hardware_simulation.md)

---

## 1. FastAPI REST API (`http://localhost:8000`)

### 1.1 Ingest SUMO Network
- **Route:** `POST /api/load`
- **Body:** `{"file_path": "/path/to/network.net.xml"}`
- **Response:** `{"status": "success", "message": "Network loaded successfully."}`

### 1.2 List Junctions
- **Route:** `GET /api/junctions`

### 1.3 Toggle Connection Failure Mode
- **Route:** `POST /api/junctions/{junction_id}/failure`
- **Body:** `{"state": true}`

### 1.4 Toggle Fixed Plans Disabling
- **Route:** `POST /api/junctions/{junction_id}/fixed-plans`
- **Body:** `{"state": true}`

### 1.5 Simulate Hardware or Software Fault
- **Route:** `POST /api/junctions/{junction_id}/simulate-error`
- **Body:** `{"category": "HARDWARE"}` *(or `"SOFTWARE"`)*

---

## 2. WebSocket Real-Time Streaming (`ws://localhost:8000/ws`)

### 2.1 State Change Event (`state_change`)
```json
{
  "type": "state_change",
  "junction_id": "J1",
  "light_id": 0,
  "state": "GREEN"
}
```

---

## 3. UTMC2 / SNMP OID Reference Table

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

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under Apache 2.0.</small>
</div>
