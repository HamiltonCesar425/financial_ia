# Financial IA

AI-driven financial health scoring system designed with production-grade architecture, including API layer, observability, containerization and simulation pipeline.

---

## Security Notes

This project uses a Python base image that may contain known vulnerabilities (1 critical, 1 high) identified by container scanning tools.

Mitigations applied:

- Updated base image to Debian Bookworm
- Removed unnecessary dependencies
- Rebuilt image with no cache

These vulnerabilities are likely inherited from upstream system packages.

For production usage:

- Continuous image scanning is recommended
- Integration with tools like Trivy or Snyk is advised

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

## Architecture

- FastAPI: ML inference API
- Prometheus: metrics collection
- Grafana: metrics visualization
- Docker Compose: orchestration

Flow:
Client → API → Metrics → Prometheus → Grafana

---

## API Example

### Request

POST /score

```json
{
  "income": 5000,
  "expenses": 3000,
  "debts": 10000
}
```

---

## Response

```json
{
  "health_score": 0.78,
  "classification": "Good"
}
```

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

**Executar com cobertura**pytest --cov=src --cov-report=term-missing

---

## Run locally

docker-compose up --build

---

## Metrics

- request_count
- request_latency
- prediction_errors

---

## Observability

The project includes instrumentation for metrics monitoring.

Metrics are exposed via `/metrics` endpoint using Prometheus client.

Examples:

- request_count_total
- request_latency_seconds
- prediction_errors_total

---

## Monitoring

- Prometheushttp://localhost:9090

- Grafanahttp://localhost:3000

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
