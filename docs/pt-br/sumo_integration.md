---
tags: [sumo, parser, xml, tllogic, pt-br]
aliases: [Integração com SUMO PT-BR, Leitura de Redes]
---

# 🗺️ Integração e Ingestão de Redes SUMO

Este documento explica como o **CARINA Mock Lights** extrai informações de geometria e semáforos a partir de malhas viárias do **Eclipse SUMO**.

⬅️ Voltar para o [Master MOC](carina_moc.md) | 🏛️ Ver [Arquitetura](architecture.md) | 🚦 Ver [Simulação de Hardware](hardware_simulation.md)

---

## 1. Suporte a Arquivos Diretos e Comprimidos

O parser aceita tanto arquivos `.net.xml` quanto arquivos comprimidos `.net.xml.gz`, descompactando em memória transparente com a biblioteca `gzip` do Python.

---

## 2. Mapeamento de `<tlLogic>`

O parser varre os nós `<tlLogic>` para construir objetos `JunctionData`:
- Duração das fases (`duration`) em segundos inteiros.
- Sequência de caracteres de estado dos focos (`state`):
  - `g`, `G`: Verde de passagem livre ou prioritário.
  - `y`, `Y`: Amarelo de transição e advertência.
  - `r`, `R`: Vermelho de retenção.
  - `u`: Amarelo intermitente.
  - `s`, `O`: Foco desligado / apagado.

Cada fase encontrada é indexada como um estágio comutável via máscaras binárias do protocolo UTMC2 ($2^k$).

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Logo Noxfort Systems" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob Apache 2.0.</small>
</div>
