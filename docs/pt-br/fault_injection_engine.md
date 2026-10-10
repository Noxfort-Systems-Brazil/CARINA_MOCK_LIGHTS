---
tags: [fault, injection, traps, snmp, errors, pt-br]
aliases: [Injeção de Falhas PT-BR, Catálogo de Falhas]
---

# ⚠️ Motor de Injeção de Falhas e Traps SNMP

Este documento detalha o sistema de injeção de falhas físicas e lógicas no **CARINA Mock Lights** e a geração de pacotes SNMPv2-Trap codificados em BER/TLV.

⬅️ Voltar para o [Master MOC](carina_moc.md) | 🚦 Ver [Simulação de Hardware](hardware_simulation.md) | ⚡ Ver [Referência de APIs](api_reference.md)

---

## 1. Catálogo de Erros Disponíveis

### 1.1 Falhas de Hardware
- **Lâmpada/LED Queimado (`LAMP_FAILURE`):** OID `1.3.6.1.4.1.2825.4.1.1` - Nível Crítico.
- **Conflito de Verdes (`GREEN_CONFLICT`):** OID `1.3.6.1.4.1.2825.4.1.2` - Nível Crítico (intervenção da matriz física).
- **Falha de Laço Indutivo (`DETECTOR_FAILURE`):** OID `1.3.6.1.4.1.2825.4.1.3` - Nível Alerta.
- **Oscilação de Energia (`POWER_ALARM`):** OID `1.3.6.1.4.1.2825.4.1.4` - Nível Alerta (operação em no-break).
- **Armário Aberto (`CABINET_DOOR`):** OID `1.3.6.1.4.1.2825.4.1.5` - Nível Alerta (violação física).

### 1.2 Falhas de Software
- **Comando Rejeitado (`COMMAND_REJECTED`):** OID `1.3.6.1.4.1.2825.4.2.1` - Nível Alerta.
- **Violação de Tempo de Segurança (`SAFETY_TIME_VIOLATION`):** OID `1.3.6.1.4.1.2825.4.2.2` - Nível Crítico.
- **Desincronização de Relógio RTC (`RTC_DRIFT`):** OID `1.3.6.1.4.1.2825.4.2.3` - Nível Alerta.
- **Erro de Plano Local (`PLAN_EXECUTION_ERROR`):** OID `1.3.6.1.4.1.2825.4.2.4` - Nível Alerta.
- **Estouro de Fila de Requisições (`QUEUE_OVERFLOW`):** OID `1.3.6.1.4.1.2825.4.2.5` - Nível Alerta.

---

## 2. Empacotamento BER/TLV e Envio UDP

O simulador monta pacotes UDP SNMPv2-Trap nativos via funções em Python puro:
- Formatação no padrão: `TRAP|<OID>|<NÍVEL>|[<CATEGORIA>] <NOME>: <MENSAGEM>`
- Despacho simultâneo para as portas UDP **162** (IANA padrão) e **1620** (ambiente não-root), permitindo que listeners do CARINA capturem as ocorrências instantaneamente.

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Logo Noxfort Systems" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob Apache 2.0.</small>
</div>
