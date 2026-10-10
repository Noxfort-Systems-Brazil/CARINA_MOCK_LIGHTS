---
tags: [readme, home, carina, mock, pt-br]
aliases: [Central de Documentação, Visão Geral PT-BR]
---

<div align="center">

<img src="../assets/carina-logo.png" alt="Logo CARINA MOCK LIGHTS" width="130" />

# CARINA MOCK LIGHTS
### Simulador de Semáforos e Servidor de Resposta UTMC2/SNMP em Alta Fidelidade
*Noxfort Systems — A State Of Art Company*

[![Status](https://img.shields.io/badge/Status-Ativo-brightgreen?style=flat&logo=github)](https://github.com/Noxfort-Systems-Brazil/CARINA)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?style=flat&logo=node.js&logoColor=white)](https://nodejs.org/)
[![React](https://img.shields.io/badge/React-19.2%2B-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![Electron](https://img.shields.io/badge/Electron-42.0%2B-47848F?style=flat&logo=electron&logoColor=white)](https://electronjs.org/)
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-Apache_2.0-blue?style=flat)](../../LICENSE)

---

🌐 **Traduções / Idiomas:** **[🇧🇷 Português do Brasil](README.md)** • **[🇺🇸 English](../../README.md)** • **[📚 Portal Principal](../index.md)**

---

</div>

O **CARINA Mock Lights** é um simulador de controladores semafóricos físicos e bancada de testes para o ecossistema **CARINA** (Controlled Artificial Road-traffic Intelligence Network Architecture). Ele processa malhas viárias do simulador Eclipse SUMO (`.net.xml`), simula grupos focais com tempos de segurança e interverdes reais, instancia agentes SNMP assíncronos em portas UDP dedicadas (1610+), dispara armadilhas SNMP Traps padrão UTMC2 para falhas de hardware/software e disponibiliza uma interface desktop moderna em **React 19 + TypeScript + Material UI + Electron**.

---

## 📚 Central de Conhecimento e Módulos Técnicos

| Cartão / Subsistema | Área de Foco | Link Direto |
| :--- | :--- | :---: |
| 📚 **Master MOC** | Índice Principal, Obsidian Vault e Mapa do Código | [Explorar Hub](carina_moc.md) |
| 🏛️ **Arquitetura do Sistema** | Concorrência, FastAPI, PySNMP e Electron | [Ver Arquitetura](architecture.md) |
| ⚡ **Referência de APIs e Protocolos** | Endpoints FastAPI REST, WebSockets e Tabela de OIDs | [Ver Referência](api_reference.md) |
| 🚦 **Simulação de Hardware** | Controladores Dataprom, Siemens, Digicon, Swarco e Kapsch | [Ver Simulação](hardware_simulation.md) |
| ⚠️ **Injeção de Falhas** | Pacotes BER/TLV, Traps SNMP, Queima de Lâmpada e Conflito | [Ver Falhas](fault_injection_engine.md) |
| 🗺️ **Integração com SUMO** | Parser de XML, Sequenciamento de Fases e Grupos Focais | [Ver Guia SUMO](sumo_integration.md) |
| 🖥️ **Interface & Dashboard** | Arquitetura React 19, Material UI, Vite e Electron | [Ver Guia UI](ui_and_dashboard.md) |
| 🛠️ **Guia do Desenvolvedor** | Setup, Modos de Execução, Testes com snmpwalk e snmpset | [Ver Guias](developer_guides.md) |
| 🧪 **Testes & Validação** | Suíte pytest, Validação de Parser e Verificação de Estados | [Ver Diretrizes](testing.md) |
| 🚀 **Empacotamento & Distribuição** | Instaladores Electron Builder e Serviço Daemon em Produção | [Ver Distribuição](deployment_and_packaging.md) |

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Logo Noxfort Systems" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob Apache 2.0.</small>
</div>
