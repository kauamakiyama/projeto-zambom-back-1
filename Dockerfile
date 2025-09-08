
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia requirements primeiro (para cache de dependências)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Expõe porta da API
EXPOSE 8000

# Comando de inicialização do FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
