---
tags: [hardware, simulation, controllers, pt-br]
aliases: [Simulação de Hardware PT-BR, Emulação de Controladores]
---

# 🚦 Simulação de Hardware e Controladores Físicos

Este documento especifica a emulação de controladores semafóricos reais no **CARINA Mock Lights**, cobrindo perfis de fabricantes, máquinas de estado de transição e firewall VPN.

⬅️ Voltar para o [Master MOC](carina_moc.md) | ⚡ Ver [Referência de APIs](api_reference.md) | ⚠️ Ver [Injeção de Falhas](fault_injection_engine.md)

---

## 1. Perfis de Fabricantes de Controladores

Os cruzamentos recebem modelos reais com strings autênticas de identificação `sysDescr`:
- **Dataprom (DP-2000 / DP-SMART):** Controlador de padrão nacional com protocolo UTMC2.
- **Siemens (ST950):** Controlador internacional de alta capacidade.
- **Digicon (CD-300):** Controlador inteligente nacional.
- **Swarco (ITC-3):** Controlador europeu robusto.
- **Kapsch (EcoController):** Controlador urbano ecológico.

---

## 2. Máquina de Estados e Tempos de Interverde

Transições diretas de Verde para Vermelho são proibidas na engenharia de tráfego. O CARINA Mock Lights implementa o ciclo de interverde:
1. **Comando Recebido:** Ao receber uma máscara de estágio alvo (`HOLD`), calcula-se a fase solicitada.
2. **Tempo Amarelo (`YELLOW`):** Os links ativos em verde recebem estado amarelo e ativam a trava de transição (`transition_lock = True`).
3. **Novo Verde:** Ao expirar o tempo de amarelo/segurança, o novo estágio é aplicado e o lock liberado.
4. **Prevenção de Oscilação:** Comandos adicionais recebidos durante o lock de transição são enfileirados ou ignorados com registro em log.

---

## 3. Modos Operacionais Especiais

- **ALERT (Amarelo Intermitente):** Focos piscam em amarelo a 1 Hz (OID `.2825.4.2.1.1.2.1.255.1`).
- **OFF (Modo Apagado):** Todos os semáforos são desligados (OID `.2825.4.2.1.1.2.1.254.1`).

---

## 4. Firewall Simulado de Sub-Rede VPN

Apenas requisições oriundas de faixas privadas (`10.x.x.x`, `127.x.x.x`, `192.168.x.x`, `172.16.x.x`) são aceitas. Pacotes externos recebem bloqueio imediato com aviso nos logs, simulando a proteção de rede de campo das prefeituras.

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Logo Noxfort Systems" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob Apache 2.0.</small>
</div>
