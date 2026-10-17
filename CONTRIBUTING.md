<!--
SPDX-FileCopyrightText: 2026 Noxfort Systems
SPDX-License-Identifier: Apache-2.0
-->

# Contributing to CARINA Mock Lights

Thank you for considering contributing to **CARINA Mock Lights**! Your contributions help build a reliable, authentic hardware testing sandbox for adaptive traffic light networks.

## Development Setup

1. Clone or navigate to the project directory.
2. Set up the Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install -e .[dev,docs]
   ```
3. Set up the UI / Electron environment:
   ```bash
   cd ui
   npm install
   ```

## Guidelines & Testing

Before submitting changes:
1. Ensure all unit tests pass:
   ```bash
   pytest tests/
   ```
2. Follow clean code and SOLID architecture principles.
3. Make sure SNMP handlers and OID responders maintain compliance with UTMC2 and NTCIP 1202 specifications.
4. Update the relevant documentation in `docs/` and `ARCHITECTURE.md` if interfaces or protocol behaviors are changed.

## Pull Request Process

1. Create a feature branch from `main`.
2. Commit your changes with clear, descriptive commit messages.
3. Ensure no regressions in SUMO parsing or PySNMP command responders.
4. Submit your Pull Request for review by the Noxfort Systems engineering team.
