---
tags: [developer, guide, setup, cli, snmp, pt-br]
aliases: [Guia do Desenvolvedor PT-BR, Instruções de Setup]
---

# 🛠️ Guia do Desenvolvedor e Testes de SNMP

Este documento orienta sobre a preparação do ambiente de desenvolvimento, execução do simulador e testes com ferramentas CLI SNMP.

⬅️ Voltar para o [Master MOC](carina_moc.md) | 🧪 Ver [Testes e Validação](testing.md) | ⚡ Ver [Referência de APIs](api_reference.md)

---

## 1. Configuração do Ambiente Local

### 1.1 Pré-requisitos
- Python 3.10+
- Node.js 20+ e npm
- Pacote `snmp` do Linux (ferramentas `snmpget`, `snmpset`, `snmptrapd`)

### 1.2 Instalação das Dependências
```bash
# Backend Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .[dev,docs]

# Frontend Electron / React
cd ui
npm install
cd ..
```

---

## 2. Modos de Execução

### 2.1 Aplicação Desktop Completa (Recomendado)
```bash
python main.py
```
Inicia o backend FastAPI e abre a janela gráfica do Electron automaticamente.

### 2.2 Modo Apenas Servidor (Headless)
```bash
python main.py --server
```
Executa apenas o FastAPI e os agentes SNMP sem abrir interface visual.

---

## 3. Testando via Terminal SNMP

### 3.1 Consultar Descrição do Modelo (`snmpget`)
```bash
snmpget -v2c -c public 127.0.0.1:1610 1.3.6.1.2.1.1.1.0
```

### 3.2 Travar no Estágio 2 (`snmpset`)
```bash
snmpset -v2c -c public 127.0.0.1:1610 1.3.6.1.4.1.2825.4.2.1.1.4.1.2.1 i 2
```

### 3.3 Ativar Amarelo Intermitente (`snmpset`)
```bash
snmpset -v2c -c public 127.0.0.1:1610 1.3.6.1.4.1.2825.4.2.1.1.2.1.255.1 i 1
```

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Logo Noxfort Systems" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob Apache 2.0.</small>
</div>
