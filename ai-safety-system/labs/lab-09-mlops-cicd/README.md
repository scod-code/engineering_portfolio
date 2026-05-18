# Lab 9 — MLOps: CI/CD Pipeline with Jenkins, Gitea, MQTT, and LLM Integration

Converted the Lab 8 simulator into a structured Python project and routed
it through a full CI/CD pipeline. Achieved BUILD SUCCESS with 9/9 tests
passing across original and LLM-generated file variants.

## Pipeline Stages
1. Checkout (from Gitea)
2. Install Dependencies (pip)
3. Test All Files (pytest with JUnit XML)
4. Generate Report (Python script)
5. Publish to MQTT (real-time broadcast)

## Key Work
- Declarative Groovy Jenkinsfile with 5 stages
- Gitea self-hosted version control
- Two local LLMs (deepcoder-1.5b, qwen2.5-coder-1.5b via Ollama) auto-generating
  improved code variants, validated against the same test suite
- REST API build trigger and polling from Jupyter
- MQTT subscriber confirming BUILD SUCCESS in real time

## Key Skills
Python, Docker, Jenkins, Gitea, MQTT (paho-mqtt), Ollama, pytest,
JUnit XML, Groovy DSL, REST API, Git workflow

## Files
- `lab09-mlops-cicd.ipynb` — Lab notebook
- `setup-instructions.pdf` — Environment setup guide
- `lab-files/` — Supporting lab files including advanced task
