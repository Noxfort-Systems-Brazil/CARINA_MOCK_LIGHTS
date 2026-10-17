---
tags: [testing, pytest, validation, unit-tests, qa]
aliases: [Testing and Validation, QA, Unit Tests]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# 🧪 Testing & Validation Strategy

This document details the test suite and quality assurance procedures for **CARINA Mock Lights**.

⬅️ Back to [Documentation Hub](CARINA_MOC.md) | 🛠️ See [Developer Guides](DEVELOPER_GUIDES.md) | 🏛️ See [System Architecture](ARCHITECTURE.md)

---

## 1. Test Architecture

The test suite is built on **pytest** and located under `tests/`:

- [`tests/test_core.py`](../tests/test_core.py): Tests individual `TrafficLight` state machine transitions, cyclic loops (`RED` $\to$ `GREEN` $\to$ `YELLOW` $\to$ `RED`), and observer dispatching.
- [`tests/test_parser.py`](../tests/test_parser.py): Validates XML DOM navigation, extraction of `<tlLogic>`, phase timing parsing, and graceful error handling on corrupt XML inputs.

---

## 2. Running Automated Tests

Run the test suite within your activated virtual environment:

```bash
pytest tests/
```

### 2.1 Verbose Mode with Coverage
```bash
pytest tests/ -v --cov=core --cov=server --cov-report=term-missing
```

---

## 3. Writing New Unit Tests

When adding new OID handlers or simulation features, follow these testing patterns:

### 3.1 State Machine Verification Example
```python
def test_traffic_light_notification():
    events = []
    class MockObserver:
        def on_state_change(self, junction_id, light_id, state):
            events.append((junction_id, light_id, state))

    light = TrafficLight(light_id=1, junction_id="J1")
    light.add_observer(MockObserver())
    light.set_state(LightState.GREEN)

    assert len(events) == 1
    assert events[0] == ("J1", 1, LightState.GREEN)
```

### 3.2 OID Handler Test Example
```python
from server.utmc_handlers import registry
from core.traffic_light import TrafficLight, LightState

def test_flash_override_handler():
    lights = [TrafficLight(0)]
    handled = registry.handle_set(".2825.4.2.1.1.2.1.255.1", 1, "J1", lights)
    assert handled is True
```

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • SPDX-License-Identifier: Apache-2.0</small>
</div>
