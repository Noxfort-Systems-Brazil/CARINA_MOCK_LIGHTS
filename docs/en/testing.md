---
tags: [testing, pytest, validation, en]
aliases: [Testing and Validation EN, QA EN]
---
<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->


# 🧪 Testing & Validation Strategy

This document describes the test suite and validation procedures for **CARINA Mock Lights**.

⬅️ Back to [Master MOC](carina_moc.md) | 🛠️ See [Developer Guides](developer_guides.md) | 🏛️ See [Architecture](architecture.md)

---

## 1. Test Suite Structure

Located in `tests/`:
- `tests/test_core.py`: Validates signal state loop transitions (`RED` $\to$ `GREEN` $\to$ `YELLOW` $\to$ `RED`) and observer event dispatches.
- `tests/test_parser.py`: Tests XML ingestion of `<tlLogic>` definitions and error resilience against corrupted network files.

---

## 2. Running Pytest

```bash
pytest tests/ -v
```

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Controlled Artificial Road-traffic Intelligence Network Architecture • CARINA MOCK LIGHTS v1.1.0</i><br/>
  <small>© 2026 Noxfort Systems • SPDX-License-Identifier: Apache-2.0</small>
</div>
