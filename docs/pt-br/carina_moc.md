---
tags: [moc, hub, docs, obsidian, carina, mock, pt-br]
aliases: [Master MOC PT-BR, Índice Geral, Mapa do Código]
---

<div align="center">

<img src="../assets/carina-logo.png" alt="Logo CARINA MOCK LIGHTS" width="120" />

# CARINA Mock Lights — Central Mestre de Documentação
### Índice Central e Base de Conhecimento do Simulador
*Noxfort Systems — A State Of Art Company*

</div>

Bem-vindo à biblioteca técnica do **CARINA Mock Lights**. Projetado como um simulador de hardware de alta fidelidade e bancada de validação UTMC2/SNMP, o CARINA Mock Lights permite realizar testes completos de algoritmos adaptativos sem a necessidade de controladores de campo físicos.

Compatível integralmente com o **GitHub** e o **[Obsidian](https://obsidian.md/)**.

---

## 🗺️ Mapa de Diretórios e Código-Fonte

```text
CARINA_MOCK_LIGHTS/
├── main.py                     # Orquestrador Master (CLI flags, resolvedor Node via NVM, launcher Electron)
├── ARCHITECTURE.md             # Blueprint Arquitetural e Topologia de Concorrência
├── pyproject.toml              # Metadados e dependências do projeto
├── requirements.txt            # Dependências Python de execução
├── sync.sh                     # Script automatizado de commit e push
├── mkdocs.yml                  # Configuração do Material for MkDocs
│
├── core/                       # Núcleo de Simulação
│   ├── traffic_light.py        # Máquina de estados dos grupos focais (RED, GREEN, YELLOW, Observer)
│   ├── sumo_parser.py          # Parser XML do SUMO (.net.xml / .net.xml.gz)
│   └── manager.py              # TrafficLightManager, ciclo dos cruzamentos, presets brasileiros e falhas
│
├── server/                     # Camada de Comunicação e Protocolos
│   ├── api.py                  # Servidor FastAPI, rotas REST, WebSocket e sincronização de loops
│   ├── utmc_server.py          # Agente PySNMP assíncrono (porta 1610+ por cruzamento)
│   ├── utmc_handlers.py        # OIDHandlerRegistry, decodificadores de máscara (HOLD, FORCE_OFF, FLASH)
│   ├── utmc_responders.py      # Respondedores Get/Set com firewall de subnet VPN
│   ├── utmc_logger.py          # Loggers dedicados de conexão e comandos
│   └── utmc_utils.py           # Utilitários de rede IP
│
├── ui/                         # Interface Desktop Moderna (Electron + React)
│   ├── electron.cjs            # Processo principal do Electron
│   ├── index.html              # Entrada HTML do Vite
│   ├── vite.config.ts          # Configuração do empacotador Vite
│   └── src/                    # Frontend React 19
│       ├── main.tsx            # Raiz da aplicação
│       ├── App.tsx             # Dashboard interativo (Material UI, WebSocket, controles)
│       └── index.css           # Estilos globais
│
├── docs/                       # Base Técnica de Conhecimento
│   ├── CARINA_MOC.md           # Master MOC em Inglês
│   ├── index.md                # Portal MkDocs
│   ├── en/                     # Hub em Inglês
│   └── pt-br/                  # Hub em Português do Brasil (Este Diretório)
│
└── tests/                      # Suíte de Testes Automatizados
    ├── test_core.py            # Testes de transição de estado
    └── test_parser.py          # Testes do parser SUMO
```

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Logo Noxfort Systems" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob Apache 2.0.</small>
</div>
