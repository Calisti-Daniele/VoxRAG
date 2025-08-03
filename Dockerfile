FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y bash curl && rm -rf /var/lib/apt/lists/*


COPY . .
RUN chmod +x start.sh

CMD ["bash", "./start.sh"]
