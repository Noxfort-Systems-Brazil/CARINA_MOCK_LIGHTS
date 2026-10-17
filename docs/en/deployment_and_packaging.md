---
tags: [deployment, packaging, electron-builder, en]
aliases: [Deployment and Packaging EN, Build Guide EN]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# 🚀 Deployment & Packaging Guide

This document describes how to build standalone installers and set up production systemd services for **CARINA Mock Lights**.

⬅️ Back to [Master MOC](carina_moc.md) | 🛠️ See [Developer Guides](developer_guides.md) | 🏛️ See [Architecture](architecture.md)

---

## 1. Electron Distributables

```bash
cd ui
npm run build
npx electron-builder --linux AppImage
```

---

## 2. Headless Systemd Deployment

```ini
[Unit]
Description=CARINA Mock Lights Headless Daemon
After=network.target

[Service]
Type=simple
User=traffic
WorkingDirectory=/opt/carina_mock_lights
ExecStart=/opt/carina_mock_lights/.venv/bin/python main.py --server
Restart=always

[Install]
WantedBy=multi-user.target
```

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • SPDX-License-Identifier: Apache-2.0</small>
</div>
