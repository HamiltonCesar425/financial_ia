# Financial IA

## Plataforma de diagnóstico financeiro com backend observável, frontend web e pipeline seguro

Financial IA é uma aplicação full stack criada para transformar dados financeiros simples em um diagnóstico rápido, legível e acionável. A proposta do projeto é unir experiência de produto, engenharia de software e práticas modernas de confiabilidade em uma solução que recebe receita, despesas e dívida, calcula um score financeiro e devolve classificação e recomendação prática.

Além da experiência do usuário, o projeto foi estruturado com foco em qualidade operacional: cobertura de testes elevada, análise estática, auditoria de dependências com lockfiles reproduzíveis e pipeline de CI preparado para evitar regressões futuras.

## Destaques do projeto

- backend em FastAPI com rotas de aplicação, saúde e métricas
- frontend em React/Vite para interação rápida e objetiva
- motor de cálculo com classificação e recomendação financeira
- camada adicional de diagnóstico estruturado via JSON e CSV
- observabilidade com Prometheus e Grafana
- suíte de testes automatizados com cobertura acima do mínimo exigido
- auditoria de dependências com `pip-audit` baseada em lockfiles
- workflow de CI consolidado com controle de concorrência para evitar filas desnecessárias

## O que a aplicação entrega

O usuário informa dados financeiros essenciais e recebe:

- score financeiro
- classificação do cenário
- recomendação prática
- diagnóstico estruturado por rota dedicada
- suporte a envio de dados também por arquivo CSV

Isso torna o projeto útil tanto como MVP de produto quanto como demonstração técnica de uma aplicação Python moderna com frontend integrado.

## Arquitetura resumida

```text
.
├── .github/workflows/ci.yml
├── frontend/
├── src/
│   ├── api/
│   │   ├── app.py
│   │   ├── business_metrics.py
│   │   ├── routes/
│   │   │   └── diagnosis.py
│   │   └── schemas.py
│   ├── domain/
│   │   ├── diagnosis_service.py
│   │   └── insights_service.py
│   ├── observability/
│   │   ├── http_metrics_middleware.py
│   │   └── registry.py
│   └── ...
├── tests/
├── requirements.txt
├── requirements-dev.txt
├── requirements.lock
├── requirements-dev.lock
└── README.md
```

## Stack técnica

### Backend

- Python 3.10
- FastAPI
- Pydantic
- scikit-learn
- hmmlearn
- Prometheus instrumentation

### Frontend

- React
- Vite

### Qualidade e segurança

- pytest
- pytest-cov
- Ruff
- Bandit
- pip-audit
- pip-tools
- GitHub Actions

## Execução local

### 1. Criar ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências reproduzíveis

Ambiente completo de desenvolvimento:

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-dev.lock
```

Apenas dependências principais:

```powershell
python -m pip install -r requirements.lock
```

### 3. Subir o backend

```powershell
uvicorn src.api.app:app --reload
```

Rotas locais:

- `http://localhost:8000/`
- `http://localhost:8000/health`
- `http://localhost:8000/docs`
- `http://localhost:8000/metrics`

Principais endpoints:

- `POST /score`
- `POST /diagnosis`
- `POST /upload/csv`

### 4. Subir o frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend local:

- `http://localhost:5173`

## Configuração de ambiente

Para conectar o frontend ao backend publicado:

```env
VITE_API_URL=https://financial-ia.onrender.com
```

Se `VITE_API_URL` não estiver definida, o frontend usa `http://localhost:8000`.

## Fluxos de diagnóstico

Além da rota principal de score, a aplicação também oferece um fluxo de diagnóstico dedicado.

### Diagnóstico via JSON

Envia receita e despesas diretamente:

```json
{
  "receita": 1000,
  "despesas": 400
}
```

Resposta esperada:

```json
{
  "score": 60,
  "message": "Situação estável",
  "recommendation": "Otimizar investimentos"
}
```

### Diagnóstico via CSV

O endpoint `POST /upload/csv` aceita arquivos com colunas:

- `receita` e `despesas`
- ou `income` e `expenses`

Isso permite evoluir a aplicação para cenários de ingestão simples sem quebrar a consistência do domínio.

## Qualidade, testes e segurança

### Lint

```powershell
python -m ruff check .
```

### Testes com cobertura

```powershell
python -m pytest --cov=src --cov-report=term-missing
```

### Segurança estática

```powershell
python -m bandit -r src -ll
```

### Auditoria de dependências

Produção:

```powershell
python -m pip_audit -r requirements.lock
```

Desenvolvimento:

```powershell
python -m pip_audit -r requirements-dev.lock
```

## Estratégia de dependências

O projeto usa dois níveis de gerenciamento:

- `requirements.txt` e `requirements-dev.txt` para dependências diretas
- `requirements.lock` e `requirements-dev.lock` para árvore completa congelada

Essa abordagem foi adotada para melhorar:

- reprodutibilidade local e no CI
- previsibilidade de instalações
- rastreabilidade de mudanças
- auditoria de segurança com menos ruído

Para regenerar os lockfiles:

```powershell
.venv\Scripts\pip-compile requirements.txt --cache-dir .pip-tools-cache --output-file requirements.lock
.venv\Scripts\pip-compile requirements-dev.txt --cache-dir .pip-tools-cache --output-file requirements-dev.lock
```

Fluxo recomendado ao atualizar dependências:

1. atualizar os arquivos base
2. regenerar os lockfiles
3. rodar lint, testes, Bandit e `pip-audit`
4. validar o CI antes de promover novas alterações

## CI/CD

O pipeline em `.github/workflows/ci.yml` foi consolidado para refletir uma rotina de engenharia mais robusta. Ele executa:

1. checkout do código
2. setup do Python com cache de `pip`
3. instalação por `requirements-dev.lock`
4. lint com Ruff
5. testes com cobertura
6. análise estática com Bandit
7. auditoria de dependências principais via `requirements.lock`
8. auditoria de dependências de desenvolvimento via `requirements-dev.lock`

O workflow também usa `concurrency` para cancelar execuções antigas da mesma branch, reduzindo filas e ruído operacional no GitHub Actions.

## Deploy

> Backend

Publicado em:

- `https://financial-ia.onrender.com`

Rotas públicas para validação:

- `https://financial-ia.onrender.com/`
- `https://financial-ia.onrender.com/health`
- `https://financial-ia.onrender.com/docs`

> Frontend

Publicado em:

- `https://financial-ia-sandy.vercel.app`

Deploy manual, se necessário:

```powershell
vercel --prod
```

## Observabilidade

O projeto inclui instrumentação para monitoramento local com:

- Prometheus
- Grafana

Organização atual:

- `src/api/business_metrics.py`: métricas de negócio e métricas usadas pelo fluxo principal da API
- `src/api/routes/diagnosis.py`: rotas dedicadas ao fluxo de diagnóstico e upload CSV
- `src/domain/diagnosis_service.py`: regra de domínio para composição do diagnóstico
- `src/domain/insights_service.py`: geração de mensagem e recomendação a partir do score
- `src/observability/registry.py`: registro central de métricas transversais de observabilidade
- `src/observability/http_metrics_middleware.py`: middleware de instrumentação HTTP

Subida com containers:

```powershell
docker-compose up --build
```

Serviços:

- API: `http://localhost:8000/docs`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

Credenciais padrão do Grafana:

- usuário: `admin`
- senha: `admin`

## Valor de portfólio

Este projeto demonstra, de forma prática:

- desenho de produto com foco em experiência e utilidade
- backend Python estruturado para produção
- integração entre frontend e API
- separação entre camada de rota, schema e domínio
- disciplina de testes e cobertura
- preocupação real com segurança de dependências
- maturidade de CI voltada para estabilidade, rastreabilidade e prevenção de regressões

Mais do que um MVP funcional, Financial IA representa uma aplicação construída com atenção tanto ao que o usuário final enxerga quanto ao que sustenta a operação por trás.

## O que eu construí e o que aprendi

Ao desenvolver este projeto, construí uma aplicação full stack capaz de transformar entradas financeiras simples em um diagnóstico com score, classificação e recomendação. Além da entrega funcional, estruturei o projeto com preocupações reais de engenharia, incluindo testes automatizados, cobertura, observabilidade, análise estática e auditoria de dependências.

Durante a evolução da aplicação, aprofundei meu entendimento sobre integração entre frontend e backend, organização de dependências Python, uso de lockfiles para reprodutibilidade, endurecimento de pipeline no GitHub Actions, modelagem de contratos com Pydantic e separação entre rotas, serviço de domínio e observabilidade. Também aprendi, na prática, a tratar segurança e confiabilidade como parte do produto, e não como etapas isoladas no fim do desenvolvimento.

O resultado final não representa apenas uma interface funcional ou uma API disponível, mas uma base mais madura, auditável e preparada para evolução contínua.

## Status atual

- aplicação funcional com frontend e backend integrados
- fluxo adicional de diagnóstico estruturado disponível via JSON e CSV
- pipeline de CI consolidado
- lockfiles versionados e auditados
- observabilidade disponível para ambiente local
- base pronta para evolução de produto e endurecimento operacional contínuo

## Aviso legal

Esta aplicação tem caráter informativo e não substitui orientação financeira profissional.
