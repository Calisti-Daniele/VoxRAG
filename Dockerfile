FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installa bash, curl, unzip
RUN apt-get update && apt-get install -y bash curl && rm -rf /var/lib/apt/lists/*

# Crea cartella encodings e scarica il file tiktoken
RUN mkdir -p /app/encodings \
  && curl -o /app/encodings/cl100k_base.tiktoken https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken

# Copia tutto il resto del progetto
COPY . .

# Rendi eseguibile lo script di avvio
RUN chmod +x start.sh

CMD ["bash", "./start.sh"]
