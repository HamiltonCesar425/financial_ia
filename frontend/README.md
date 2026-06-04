# Frontend - Financial IA

Interface web do MVP **Financial IA**, publicada em:

<https://financial-ia-sandy.vercel.app>

Status: Produção Inicial (Founder Release) - disponível para testes públicos.

## Função do Frontend

O frontend coleta dados financeiros essenciais, consome a API do backend e apresenta:

- diagnóstico financeiro automatizado
- score financeiro
- classificação de risco
- alertas e recomendações iniciais
- projeção financeira de 30 dias
- histórico local de análises
- gráfico interativo de evolução do score
- formulário de feedback
- páginas de privacidade e contato

## Stack

- React
- Vite
- React Router
- Recharts
- Axios
- CSS/Tailwind utilities

## Estrutura Principal

```text
src/
├── components/
├── features/
│   └── essential-diagnosis/
│       ├── components/
│       └── pages/
├── services/
├── utils/
├── App.jsx
└── main.jsx
```

## Execução Local

```powershell
npm install
npm run dev
```

Frontend local:

<http://localhost:5173>

## Variáveis de Ambiente

Crie um arquivo `.env.local` na raiz do frontend:

```env
VITE_API_URL=http://localhost:8000
```

Para produção:

```env
VITE_API_URL=https://financial-ia.onrender.com
```

## Scripts

```powershell
npm run dev
npm run lint
npm run build
npm run preview
```

## Rotas da Interface

```text
/           Home
/collection Coleta de dados financeiros
/result     Resultado do diagnóstico
/feedback   Feedback do usuário
/privacy    Privacidade
/contact    Contato
```

## Integração com API

Endpoints consumidos:

```text
GET  /health
POST /score
POST /feedback
```

## Observações de Produto

O frontend mantém o histórico de análises no navegador via `localStorage`, permitindo exibir evolução do score e gráfico histórico sem exigir autenticação nesta fase do MVP.

A aplicação possui caráter informativo e educacional e não substitui orientação financeira profissional.
