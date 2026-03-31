# Financial IA

API em **FastAPI** para análise financeira, com observabilidade integrada via **Prometheus** e **Grafana**.

---

## 🚀 Como subir os containers

Para iniciar todos os serviços (API, Prometheus e Grafana), execute:

```bash
docker-compose up --build
```

---

Isso vai construir as imagens e subir os containers definidos no docker-compose.yml.

---
---

## 📊 Acessando os serviços

. API FastAPI

  . Documentação: ```http://localhost:8000/docs```

  . Health check: ``http://localhost:8000/health``

  . Métricas Prometheus: ``http://localhost:8000/metrics``

---
. Prometheus

  . Interface: ``http://localhost:9090``

  . Targets: ``http://localhost:9090/targets``

---
. Grafana

  . Interface: ``http://localhost:3000``

  . Usuário padrão: admin

  . Senha padrão: admin (solicita alteração no primeiro login)

---

## 📈 Importando dashboards no Grafana

1. Acesse o Grafana em ``http://localhost:3000.``

2. Vá em Dashboards → Import.

3. Cole o JSON do dashboard customizado (exemplo abaixo) ou faça      upload do arquivo .json.

4. Selecione o data source Prometheus.

5. Clique em Import.

---

## 🖼️ Exemplo de JSON de dashboard

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
---

## ✅ Resultado esperado

. Após importar o dashboard, você terá:

. Total de predições realizadas

. Número de erros de predição

. Estado do modelo (sucesso vs erro)

. Latência e métricas de requisições (se adicionar painéis extras)

---
