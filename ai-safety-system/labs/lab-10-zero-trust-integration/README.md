# Lab 10 — Zero-Trust Behavioural Monitoring: Architecture and Systems Integration

Guided integration lab connecting all previous components into a single
coherent zero-trust code analysis pipeline deployed via Docker Compose.

## Five-Container Stack
1. sandbox — isolated code execution environment
2. monitor — behavioural analysis service
3. ollama — locally-running language model
4. mongodb — document database for audit storage
5. comp40771 — development workspace

## Key Work
- Full telemetry collection across six endpoints:
  /monitor/cpu, /monitor/network, /monitor/files,
  /monitor/threads, /monitor/storage, /telemetry/events/recent
- Risk scoring with weighted severity levels (HIGH 0.6, MEDIUM 0.4, LOW 0.2)
- Structured report generation with evidence-linked explanations
- MongoDB audit persistence under unique run_id
- Ollama LLM contextualised natural-language risk summaries

## Key Skills
Python, Docker Compose, MongoDB, Ollama, REST API consumption,
psutil, pymongo, risk scoring, explainable AI, systems integration

## Files
- `lab10-zero-trust-integration.ipynb` — Lab notebook
- `lab-guide.pdf` — Lab guide PDF
- `instructions.pdf` — Full lab instructions
- `mongodb-guide.pdf` — MongoDB integration reference
- `notebook-summary.pdf` — Notebook walkthrough summary
- `lab-files/` — Supporting lab files including Docker Compose stack
