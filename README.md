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

Frontend publicado:

```text
https://financial-ia-sandy.vercel.app
```

Backend publicado:

```text
https://financial-ia.onrender.com
```

---

## 🌐 Variável de ambiente do frontend

Para o frontend publicado e para testes locais com a API em nuvem, a variável `VITE_API_URL` deve apontar para o backend correto:

```env
VITE_API_URL=https://financial-ia.onrender.com
```

Observação:

* Se `VITE_API_URL` não estiver definida, o frontend usa `http://localhost:8000`
* Em produção na Vercel, a variável precisa estar configurada com a URL pública do backend

---

## 🚢 Fluxo oficial de deploy

### Backend no Render

Objetivo: publicar a API FastAPI em produção.

Passos:

1. Fazer commit das mudanças do backend
2. Dar `push` para a branch conectada ao Render, atualmente `main`
3. Verificar no Render se o deploy automático iniciou
4. Se necessário, usar:
   * `Manual Deploy`
   * `Clear build cache & deploy`
5. Validar as rotas públicas:

```text
https://financial-ia.onrender.com/
https://financial-ia.onrender.com/health
https://financial-ia.onrender.com/docs
```

Fluxo local típico:

```bash
git add .
git commit -m "Sua mensagem"
git push origin main
```

### Frontend na Vercel

Objetivo: publicar a interface React conectada ao backend correto.

Passos:

1. Fazer commit das mudanças do frontend
2. Dar `push` para `main`
3. Se necessário, publicar manualmente:

```bash
vercel --prod
```

4. Validar a aplicação publicada:

```text
https://financial-ia-sandy.vercel.app
```

Observação:

* O deploy deve ser feito a partir da raiz do projeto
* Não executar `vercel --prod` dentro de `frontend` se o projeto Vercel estiver configurado com root directory `frontend`

### Atualização de variáveis de ambiente

Objetivo: garantir que o frontend use a URL correta do backend.

Variável principal:

```env
VITE_API_URL=https://financial-ia.onrender.com
```

Quando atualizar:

* mudança de domínio do backend
* troca de ambiente
* migração de serviço no Render

Fluxo na Vercel:

1. Remover variável antiga, se necessário:

```bash
vercel env rm VITE_API_URL production
vercel env rm VITE_API_URL preview
vercel env rm VITE_API_URL development
```

2. Recriar a variável:

```bash
vercel env add VITE_API_URL production
vercel env add VITE_API_URL preview
vercel env add VITE_API_URL development
```

3. Puxar localmente para conferência:

```bash
vercel env pull .env.local
Get-Content .\.env.local
```

4. Fazer novo deploy:

```bash
vercel --prod
```

### Ordem recomendada quando backend e frontend mudam

1. Publicar o backend no Render
2. Validar o backend público
3. Atualizar `VITE_API_URL` se necessário
4. Publicar o frontend na Vercel
5. Validar o fluxo completo no navegador

### Checklist rápido de validação

Backend:

* `/` responde
* `/health` responde
* `/docs` abre

Frontend:

* landing page carrega
* formulário envia
* score aparece
* classificação aparece
* recomendação aparece

Integração:

* sem erro de CORS
* sem erro de URL inválida
* sem falha de conexão com o servidor

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
