---
tags: [api, reference, rest, websocket, snmp, pt-br]
aliases: [Referência de API PT-BR, Tabela de OIDs]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# ⚡ Referência de APIs e Protocolos

Este documento detalha as interfaces de comunicação do **CARINA Mock Lights**: API REST (FastAPI), WebSockets e tabela de OIDs UTMC2 / SNMP.

⬅️ Voltar para o [Master MOC](carina_moc.md) | 🏛️ Ver [Arquitetura](architecture.md) | 🚦 Ver [Simulação de Hardware](hardware_simulation.md)

---

## 1. Endpoints FastAPI REST (`http://localhost:8000`)

### 1.1 Carregar Malha Viária SUMO
Carrega e instancia cruzamentos a partir de uma rede SUMO.
- **Rota:** `POST /api/load`
- **Corpo:** `{"file_path": "/caminho/absoluto/rede.net.xml"}`
- **Resposta:** `{"status": "success", "message": "Network loaded successfully."}`

### 1.2 Listar Cruzamentos Ativos
Retorna status dos semáforos, portas SNMP e fabricantes de todos os cruzamentos.
- **Rota:** `GET /api/junctions`

### 1.3 Alternar Modo de Falha de Comunicação
Simula queda de link físico (o respondedor ignora solicitações SNMP).
- **Rota:** `POST /api/junctions/{junction_id}/failure`
- **Corpo:** `{"state": true}`

### 1.4 Alternar Execução de Planos Fixos Locais
Pausa o avanço automático dos tempos locais para permitir controle exclusivo externo.
- **Rota:** `POST /api/junctions/{junction_id}/fixed-plans`
- **Corpo:** `{"state": true}`

### 1.5 Simular Falha de Hardware ou Software
Dispara uma falha do catálogo e emite um pacote SNMP Trap via UDP 162/1620.
- **Rota:** `POST /api/junctions/{junction_id}/simulate-error`
- **Corpo:** `{"category": "HARDWARE"}` *(ou `"SOFTWARE"`)*

---

## 2. Streaming em Tempo Real via WebSocket (`ws://localhost:8000/ws`)

### 2.1 Mudança de Estado de Foco (`state_change`)
Disparado imediatamente quando um semáforo muda de cor:
```json
{
  "type": "state_change",
  "junction_id": "J1",
  "light_id": 0,
  "state": "GREEN"
}
```

---

## 3. Tabela de OIDs UTMC2 / SNMP

| Função | Padrão OID ASN.1 | Tipo | Operação | Descrição |
| :--- | :--- | :---: | :---: | :--- |
| **Identificação** | `1.3.6.1.2.1.1.1.0` | `OCTET STRING` | `GET` | Descrição do modelo do controlador e firmware |
| **Trava de Estágio** | `.2825.4.2.1.1.4.1.2.1` | `INTEGER` | `SET` | Máscara binária do estágio a reter (`HOLD`) |
| **Forçar Término** | `.2825.4.2.1.1.4.1.3.1` | `INTEGER` | `SET` | Força encerramento do estágio para amarelo |
| **Omitir Estágio** | `.2825.4.2.1.1.4.1.7.1` | `INTEGER` | `SET` | Omite estágio da sequência de rotação |
| **Extensão de Verde**| `.2825.4.2.1.1.4.1.6.1`| `INTEGER` | `SET` | Estende janela de verde |
| **Demanda de Tráfego**| `.2825.4.2.1.1.4.1.5.1`| `INTEGER` | `SET/GET`| Máscara de demanda de veículos |
| **Amarelo Piscante** | `.2825.4.2.1.1.2.1.255.1` | `INTEGER` | `SET` | Sobrescreve para modo de alerta intermitente |
| **Modo Apagado** | `.2825.4.2.1.1.2.1.254.1` | `INTEGER` | `SET` | Desliga todos os focos do cruzamento |
| **Estágio Ativo** | `.2825.4.2.1.1.4.1.4.1` | `INTEGER` | `GET` | Máscara binária do estágio verde em exibição |
| **Estágio em Saída** | `.2825.4.2.1.1.4.1.8.1` | `INTEGER` | `GET` | Estágio em transição amarela |

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Logo Noxfort Systems" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • Licenciado sob Apache-2.0 • SPDX-License-Identifier: Apache-2.0</small>
</div>
