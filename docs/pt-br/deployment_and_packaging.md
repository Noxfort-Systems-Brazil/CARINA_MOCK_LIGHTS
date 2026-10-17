---
tags: [deployment, packaging, electron-builder, pt-br]
aliases: [Empacotamento e Implantação PT-BR, Deploy]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# 🚀 Empacotamento e Implantação

Este documento aborda a geração de instaladores da aplicação Electron e a execução contínua em servidores através de serviços Systemd.

⬅️ Voltar para o [Master MOC](carina_moc.md) | 🛠️ Ver [Guia do Desenvolvedor](developer_guides.md) | 🏛️ Ver [Arquitetura](architecture.md)

---

## 1. Empacotamento da Interface Electron

Utiliza-se o **electron-builder** a partir da pasta `ui/`:

```bash
cd ui
npm run build
npx electron-builder --linux AppImage
```

Os executáveis gerados estarão disponíveis em `ui/dist/` ou `ui/dist-electron/`.

---

## 2. Implantação em Servidor (Systemd)

Para servidores headless sem ambiente gráfico X11:

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
  <img src="../assets/noxfort-logo.png" alt="Logo Noxfort Systems" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • Licenciado sob Apache-2.0 • SPDX-License-Identifier: Apache-2.0</small>
</div>
