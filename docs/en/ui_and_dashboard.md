---
tags: [ui, dashboard, react, electron, material-ui, en]
aliases: [UI and Dashboard EN, Electron Desktop EN]
---

# 🖥️ UI & Electron Dashboard Architecture

This document describes the graphical user interface architecture of **CARINA Mock Lights**.

⬅️ Back to [Master MOC](carina_moc.md) | 🏛️ See [Architecture](architecture.md) | ⚡ See [API Reference](api_reference.md)

---

## 1. Stack Overview

- **Electron 42:** Desktop window wrapper and background process runner.
- **React 19:** Functional UI components and reactive state hooks.
- **TypeScript 5.6:** Typed communication payloads and junction models.
- **Material UI 9:** Dark slate styled interface components.
- **Vite 8:** Modern development and bundling toolchain.

---

## 2. Real-Time Streaming Architecture

- Connects to `ws://localhost:8000/ws` on application mount.
- Dispatches granular state mutations on `state_change` messages without full page re-renders.

---

## 3. Interactive Controls

- **Network Ingestion:** Dialog to load any `.net.xml` file on disk.
- **Junction Monitor Card:** Live signal head colors, connection state, IP/Port chip, failover toggle, fixed plan disable switch, and fault injection buttons.

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under Apache 2.0.</small>
</div>
