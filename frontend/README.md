# Frontend - Diagnóstico Financeiro Automatizado

Interface do MVP do produto **Diagnóstico Financeiro Automatizado**, responsável por coletar dados do usuário e consumir a API `/score` do backend (`financial_ia`).

---

## 📌 Pré-requisitos

* Node.js >= 18
* Backend FastAPI rodando em `http://localhost:8000`

---

## ⚙️ Setup

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install axios
```

---

## 🧱 Estrutura

```bash
src/
 ├── components/
 │    ├── HeroSection.jsx
 │    ├── ValueHighlights.jsx
 │    ├── ScoreForm.jsx
 │    ├── ResultCard.jsx
 │    └── ErrorNotice.jsx
 ├── services/api.js
 ├── App.jsx
 └── main.jsx
```

---

## ▶️ Execução

```bash
npm run dev
```

Frontend disponível em:

```
http://localhost:5173
```

---

## 🔗 Integração com API

Endpoint consumido:

```
POST /score
```

### Payload enviado

```json
{
  "receita": 5000,
  "despesas": 3000,
  "divida": 1000
}
```

### Resposta esperada

```json
{
  "score": 75,
  "classificacao": "Boa",
  "recomendacao": "Reduza despesas variáveis"
}
```

---

## 🌐 Variáveis de ambiente

Crie um arquivo `.env` na raiz do frontend:

```
VITE_API_URL=http://localhost:8000
```

---

## ⚠️ Tratamento de erros

O frontend trata:

* `422` → Dados inválidos
* `500` → Erro interno do servidor
* Falha de rede → API indisponível

---

## 🧠 Comportamento da aplicação

* Validação local antes da requisição
* Botão desabilitado durante envio
* Estado de loading: *"Analisando seus dados..."*
* Scroll automático para resultado
* Possibilidade de refazer análise sem reload

---

## 📌 Observação

Este MVP tem foco em **automação simples e confiável**.

Não representa um sistema avançado de inteligência artificial nesta versão.

---
