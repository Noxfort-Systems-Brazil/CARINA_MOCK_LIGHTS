---
tags: [developer, guide, setup, cli, debugging, snmp, snmpwalk, snmpset]
aliases: [Developer Guides, Setup Guide, Testing SNMP]
---

# 🛠️ Developer Guides & Testing Setup

This document provides step-by-step instructions for configuring your local development environment, running backend and frontend services, and debugging SNMP communication.

⬅️ Back to [Documentation Hub](CARINA_MOC.md) | 🧪 See [Testing & Validation](TESTING.md) | ⚡ See [API & Protocols](API_REFERENCE.md)

---

## 1. Local Environment Setup

### 1.1 Prerequisites
- **Linux (Ubuntu/Debian recommended) or macOS / Windows with WSL2**
- **Python 3.10+**
- **Node.js 20+** and **npm**
- **Net-SNMP utilities** (for CLI debugging: `snmpwalk`, `snmpset`, `snmptrapd`)

### 1.2 System Dependencies Installation (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip snmp snmpd libsnmp-dev
```

### 1.3 Virtual Environment Setup
```bash
# In CARINA_MOCK_LIGHTS root:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .[dev,docs]
```

### 1.4 Frontend Setup
```bash
cd ui
npm install
cd ..
```

---

## 2. Running Options

### 2.1 Complete Application (Electron + FastAPI)
```bash
python main.py
```
*Automatically resolves Node version via NVM if necessary, starts the Vite development server, launches FastAPI on port 8000, and displays the Electron desktop window.*

### 2.2 Headless Backend (Servers Only)
For CI/CD pipelines, Docker containers, or headless remote testing:
```bash
python main.py --server
```
*Binds FastAPI to `0.0.0.0:8000` and creates UDP SNMP sockets for any loaded SUMO network.*

### 2.3 Independent Frontend Development
If you prefer running Vite in your browser directly:
```bash
# Terminal 1: Backend
python main.py --server

# Terminal 2: UI
cd ui
npm run dev
# Access http://localhost:5173
```

---

## 3. Debugging SNMP with Net-SNMP CLI

You can interact with the mock junctions directly from the command line using standard Net-SNMP tools.

### 3.1 Query System Description (`snmpget`)
```bash
snmpget -v2c -c public 127.0.0.1:1610 1.3.6.1.2.1.1.1.0
```
**Expected Output:**
```text
SNMPv2-MIB::sysDescr.0 = STRING: Dataprom DP-2000 Traffic Light Controller UTMC2 v3.1
```

### 3.2 Query Currently Active Stage (`snmpget`)
```bash
snmpget -v2c -c public 127.0.0.1:1610 1.3.6.1.4.1.2825.4.2.1.1.4.1.4.1
```
**Output:** Integer bitmask (e.g., `1` for Stage 1, `2` for Stage 2, `4` for Stage 3).

### 3.3 Hold Stage 2 (`snmpset`)
To hold Stage 2 active (mask = $2^1 = 2$):
```bash
snmpset -v2c -c public 127.0.0.1:1610 1.3.6.1.4.1.2825.4.2.1.1.4.1.2.1 i 2
```

### 3.4 Command Amber Flash (`snmpset`)
To switch the intersection into Alert Flashing Yellow mode:
```bash
snmpset -v2c -c public 127.0.0.1:1610 1.3.6.1.4.1.2825.4.2.1.1.2.1.255.1 i 1
```

### 3.5 Listening for Injected SNMP Traps (`snmptrapd`)
To observe fault traps emitted by the simulator:
```bash
sudo snmptrapd -f -Lo -c /dev/null --disableAuthorization=yes udp:1620
```

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under Apache 2.0.</small>
</div>
