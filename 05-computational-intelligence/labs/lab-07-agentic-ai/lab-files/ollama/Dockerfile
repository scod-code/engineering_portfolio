FROM ollama/ollama:latest

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV OLLAMA_MODELS="llama3.2:1b phi3:mini"

ENTRYPOINT ["/entrypoint.sh"]