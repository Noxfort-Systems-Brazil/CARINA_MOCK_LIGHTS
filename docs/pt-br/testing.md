---
tags: [testing, pytest, validation, pt-br]
aliases: [Testes e Validação PT-BR, QA]
---

# 🧪 Testes e Validação

Este documento orienta sobre a execução da suíte de testes unitários do **CARINA Mock Lights**.

⬅️ Voltar para o [Master MOC](carina_moc.md) | 🛠️ Ver [Guia do Desenvolvedor](developer_guides.md) | 🏛️ Ver [Arquitetura](architecture.md)

---

## 1. Suíte de Testes

Os testes são organizados na pasta `tests/` e utilizam o **pytest**:
- `tests/test_core.py`: Valida transições cíclicas da máquina de estados dos semáforos (`RED` $\to$ `GREEN` $\to$ `YELLOW` $\to$ `RED`) e disparo de eventos para observadores.
- `tests/test_parser.py`: Valida a ingestão de XML do SUMO, leitura de nós `<tlLogic>` e resiliência a arquivos inválidos.

---

## 2. Executando os Testes

Com o ambiente virtual ativado:
```bash
pytest tests/ -v
```

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Logo Noxfort Systems" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob Apache 2.0.</small>
</div>
