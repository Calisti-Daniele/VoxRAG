#!/bin/bash

echo "📦 Aspetto che Ollama e Chroma siano pronti..."
sleep 10

echo "📥 Controllo se il modello Mistral è installato..."
if ! curl -s http://ollama:11434/api/tags | grep -q "mistral"; then
    echo "⬇️  Installo Mistral in Ollama..."
    curl -X POST http://ollama:11434/api/pull -d '{"name": "mistral"}' -H "Content-Type: application/json"
else
    echo "✅ Modello Mistral già presente"
fi

if [ "$ENV" = "dev" ]; then
    echo "🛠 Avvio FastAPI in modalità sviluppo..."
    exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload --timeout-keep-alive 60
else
    echo "🚀 Avvio FastAPI in modalità produzione..."
    exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 --timeout-keep-alive 60
fi

