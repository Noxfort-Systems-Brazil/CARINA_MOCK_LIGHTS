---
tags: [deployment, packaging, electron-builder, production, systemd]
aliases: [Deployment and Packaging, Build Guide, Production Setup]
---

# 🚀 Deployment & Packaging Guide

This document describes how to package and deploy **CARINA Mock Lights** for production and testing environments.

⬅️ Back to [Documentation Hub](CARINA_MOC.md) | 🛠️ See [Developer Guides](DEVELOPER_GUIDES.md) | 🏛️ See [System Architecture](ARCHITECTURE.md)

---

## 1. Packaging the Electron Desktop Application

The graphical desktop client uses **electron-builder** to generate standalone distributable packages for Linux, macOS, and Windows.

### 1.1 Building UI Assets
```bash
cd ui
npm run build
```
*Compiles TypeScript and generates optimized static production assets into `ui/dist/`.*

### 1.2 Creating the Electron Distributable
```bash
# In ui/ folder:
npx electron-builder --linux AppImage
# Or for Debian packages:
npx electron-builder --linux deb
```
The resulting installation bundle is generated in `ui/dist-electron/` or `ui/dist/`.

---

## 2. Deploying Headless Daemon (Systemd)

In continuous integration servers or central testing nodes where a display server (X11 / Wayland) is absent, deploy the backend as a headless systemd service.

### 2.1 Service Definition (`/etc/systemd/system/carina-mock-lights.service`)
```ini
[Unit]
Description=CARINA Mock Lights Headless Simulator
After=network.target

[Service]
Type=simple
User=traffic
WorkingDirectory=/opt/carina_mock_lights
ExecStart=/opt/carina_mock_lights/.venv/bin/python main.py --server
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

### 2.2 Enabling & Starting the Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now carina-mock-lights
sudo systemctl status carina-mock-lights
```

---

## 3. Network Ports & Firewall Permissions

Ensure the following firewall rules are configured on the deployment host:

```bash
# Allow FastAPI REST & WebSockets
sudo ufw allow 8000/tcp

# Allow UTMC2 SNMP Responders (range 1610 to 1650 UDP)
sudo ufw allow 1610:1650/udp

# Allow SNMP Traps
sudo ufw allow 162/udp
sudo ufw allow 1620/udp
```

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under Apache 2.0.</small>
</div>
