# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Variáveis de ambiente para evitar a criação de arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema, incluindo libpq (necessária para psycopg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
    
# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que o Gunicorn irá rodar
EXPOSE 5000

# Comando para iniciar a aplicação em produção
# CMD ["bash", "-c", "flask db upgrade && gunicorn --bind 0.0.0.0:5000 app.main:create_app()"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:create_app()"]
