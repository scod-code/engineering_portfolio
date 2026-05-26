#!/bin/sh
set -eu

# Start Ollama server in the background
ollama serve &
SERVER_PID="$!"

# Wait until the server is ready
i=0
until ollama list >/dev/null 2>&1; do
  i=$((i+1))
  if [ "$i" -ge 60 ]; then
    echo "Ollama server did not become ready in time." >&2
    kill "$SERVER_PID" 2>/dev/null || true
    exit 1
  fi
  sleep 1
done

# Pull required models (fast if already cached in the volume)
for m in $OLLAMA_MODELS; do
  echo "Ensuring model is available: $m"
  ollama pull "$m"
done

# Stay running (keep server in foreground)
wait "$SERVER_PID"
