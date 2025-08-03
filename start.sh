#!/bin/bash
# Avvia l'app FastAPI in modalità produzione
echo "Aspetto che i servizi siano pronti..."
sleep 5  # eventualmente metti healthcheck o curl

exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 --timeout-keep-alive 60
