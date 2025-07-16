# Estágio 1: Build
FROM python:3.11-slim as builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Estágio 2: Final
FROM python:3.11-slim

# Define o diretório de trabalho DENTRO do contêiner
WORKDIR /app

# Copia o ambiente virtual com as dependências
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia todo o nosso código (index.py, public/, routes/, etc.) para o diretório de trabalho /app
COPY . .

# Expõe a porta que a aplicação vai usar
EXPOSE 8080

# Comando para iniciar a aplicação, sendo explícito sobre o diretório de trabalho
# A MUDANÇA ESTÁ AQUI: Adicionamos --app-dir . para forçar o Uvicorn a procurar no diretório atual
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8080"]

