FROM python:3.11-slim

# Evita buffer e melhora logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema (mínimo necessário)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primeiro (cache inteligente)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia restante do projeto
COPY . .

# Expõe porta da API
EXPOSE 8000

# Comando de execução
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]