# Financial IA

AI-driven financial health scoring system designed to evaluate financial conditions through quantitative indicators, simulation models and structured scoring logic.

The project combines financial metrics, scoring engines and simulation components to estimate a **financial health score** and classify financial conditions in a structured and extensible architecture.

---

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![Coverage](https://img.shields.io/badge/coverage-22%25-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## Features

- Financial health scoring algorithm
- Modular financial metrics engine
- Pillar-based scoring architecture
- Simulation engine for financial scenarios
- REST API for score calculation
- Observability with metrics instrumentation
- Automated test suite with pytest

---

## Project Architecture

financial_ia/
│
├── src/
│   ├── api/                # REST API layer
│   ├── core/               # Core scoring logic
│   ├── engine/             # Financial calculation engine
│   ├── simulation/         # Scenario simulation
│   ├── observability/      # Metrics and logging
│   ├── main.py             # Application entrypoint
│   └── __version__.py
│
├── tests/                  # Test suite
│
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── README.md

---

## Tech Stack

- Python 3.10
- FastAPI
- Pytest
- Pytest-Cov
- Docker
- Prometheus (metrics instrumentation)
- Grafana (monitoring dashboards)

---

## Installation

Clone the repository:

git clone https://github.com/HamiltonCesar425/financial_ia.git

cd financial_ia

---

## Crie ambiente virtual

python -m venv .venv

---

## Ative o ambiente virtual no Windowns

.venv/bin/activate

---

## Linux/macOS

source .venv/bin/activate

---

## Instale dependências:

pip install -r requirements.txt

---

## Running Tests

pytest

**Ececutar com cobertura**
pytest --cov=src --cov-report=term-missing

---

## Observability

The project includes instrumentation for metrics monitoring.

Metrics can be collected using **Prometheus** and visualized through **Grafana dashboards**, enabling monitoring of model behavior and system performance.

---

## Roadmap

Planned improvements:

- Expand test coverage across engine modules
- Implement full Grafana dashboards
- Add backtesting module
- CI/CD pipeline integration
- Cloud deployment
  
---

## Project Status

Active development.

The current version includes the core scoring engine, simulation components, API structure and initial test suite.

---
