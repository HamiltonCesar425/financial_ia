# Financial IA

## 📊 Diagnóstico Financeiro Automatizado

***Entenda sua saúde financeira em menos de 1 minuto**

Este projeto evoluiu para um MVP funcional que permite ao usuário:

* Informar receita, despesas e dívida
* Receber um score financeiro
* Obter classificação e recomendação prática

---

## 🚀 Como rodar o projeto

### Backend (FastAPI)

```bash
uvicorn src.api.app:app --reload
```

Acesse:

``http://localhost:8000/docs``

---

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Acesse:

``http://localhost:5173``

---

## 🔗 Integração

Endpoint principal:

```
POST /score
```

---

## 📈 Funcionalidades do MVP

* Validação de entrada (frontend + backend)
* Cálculo de score financeiro
* Classificação automática
* Recomendação prática
* Interface web responsiva

---

## ⚠️ Aviso Legal

Esta análise tem caráter informativo e não substitui orientação financeira profissional.

---

## 🔍 Observabilidade (nível avançado)

Este projeto também possui infraestrutura para monitoramento com:

* Prometheus
* Grafana

---

## 🚀 Como subir os containers

```bash
docker-compose up --build
```

---

## 📊 Acessando os serviços

### API FastAPI

```
* http://localhost:8000/docs

* http://localhost:8000/health

* http://localhost:8000/metrics

```

### Prometheus

```
* http://localhost:9090 

```

---

### Grafana

```
* http://localhost:3000

Usuário: admin
Senha: admin

```

---

## 📈 Dashboards

```json
{
  "title": "Financial IA Dashboard",
  "panels": [
    {
      "type": "stat",
      "title": "Total de Predições",
      "targets": [{ "expr": "prediction_total" }],
      "gridPos": { "x": 0, "y": 0, "w": 8, "h": 6 }
    },
    {
      "type": "stat",
      "title": "Erros de Predição",
      "targets": [{ "expr": "prediction_errors_total" }],
      "gridPos": { "x": 8, "y": 0, "w": 8, "h": 6 }
    },
    {
      "type": "barchart",
      "title": "Estado do Modelo",
      "targets": [{ "expr": "model_state_total" }],
      "gridPos": { "x": 0, "y": 6, "w": 16, "h": 8 }
    }
  ]
}
```

---

## 📌 Status do Projeto

✔ MVP funcional (frontend + backend)
✔ Integração completa
✔ Observabilidade com Prometheus/Grafana
⬜ Persistência de dados

---

## 🎯 Próximos passos

* Persistência de diagnósticos
* Dashboard analítico
* Deploy em nuvem
