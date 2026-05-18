FROM ollama/ollama:latest

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV OLLAMA_MODELS="deepcoder:1.5b qwen2.5-coder:1.5b"

ENTRYPOINT ["/entrypoint.sh"]