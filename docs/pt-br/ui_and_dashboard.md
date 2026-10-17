---
tags: [ui, dashboard, react, electron, material-ui, pt-br]
aliases: [Interface Gráfica PT-BR, Dashboard Electron]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# 🖥️ Interface Gráfica e Dashboard Electron

Este documento descreve a arquitetura da interface desktop moderna do **CARINA Mock Lights**.

⬅️ Voltar para o [Master MOC](carina_moc.md) | 🏛️ Ver [Arquitetura](architecture.md) | ⚡ Ver [Referência de APIs](api_reference.md)

---

## 1. Stack Tecnológica

- **Electron 42:** Executável desktop nativo multiplataforma (Linux, macOS, Windows).
- **React 19:** Componentes funcionais e reatividade rápida com hooks.
- **TypeScript 5.6:** Tipagem estática rigorosa para payloads e estados.
- **Material UI 9 (MUI):** Biblioteca de componentes elegantes em tema escuro.
- **Vite 8:** Compilação rápida e Hot Module Replacement (HMR).

---

## 2. Comunicação e Atualização em Tempo Real

1. O frontend conecta-se via WebSocket (`ws://localhost:8000/ws`).
2. O servidor FastAPI despacha eventos `state_change` instantaneamente para todos os clientes conectados.
3. A interface atualiza o grupo focal sem recarregar a árvore inteira de componentes DOM.

---

## 3. Controles Disponíveis no Painel

- **Botão de Carregar Rede SUMO:** Abre caixa de diálogo para seleção de arquivos `.net.xml`.
- **Card de Cruzamento:**
  - Identificação, fabricante/modelo e status da conexão.
  - Endereço IP/Porta UDP do respondedor SNMP com cópia para a área de transferência.
  - Grade visual dos focos semafóricos com cores dinâmicas.
  - Interruptores de modo de falha de conexão e desativação de planos fixos.
  - Botões rápidos de injeção de falhas de hardware e software.

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Logo Noxfort Systems" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • Licenciado sob Apache-2.0 • SPDX-License-Identifier: Apache-2.0</small>
</div>
