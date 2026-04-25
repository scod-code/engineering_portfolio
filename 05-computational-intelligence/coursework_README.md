# Zero-Trust Adaptive Code Safety Harness — COMP40771

**Student:** Somtochukwu C. Osigwe-Daniel  
**ID:** N1419979  
**Module:** COMP40771 Computational Intelligence  

---

## 1. Project Overview

This project implements an Adaptive Code Safety Harness that evaluates 
untrusted code without inspecting its logic directly. It combines Static 
AST Analysis with Dynamic Runtime Telemetry (CPU stress, network activity, 
filesystem tampering) to produce a weighted, explainable risk score.

Computational Intelligence techniques used:
- Genetic Algorithm (GA) — probe selection optimisation
- Particle Swarm Optimisation (PSO) — configuration tuning
- Reinforcement Learning (RL) — adaptive probe policy
- Multi-Agent MQTT Orchestration — distributed decision fusion

---

## 2. Prerequisites

- Docker Desktop installed and running
- Port 8081 free (Jupyter), Port 1883 free (MQTT), Port 8030 free (API Sandbox)
- Git (for Olympus access)

---

## 3. Deployment — Quick Start

From the root of this repository, run:
```bash
docker-compose up -d
```

This launches:
| Container | Purpose | Port |
|---|---|---|
| comp40771_cwk | Jupyter notebook environment | 8081 |
| mqtt-broker | MQTT message broker | 1883 |

Then launch the API Sandbox container separately:
```bash
docker run -d --rm \
  -p 8030:8000 -p 8501:8501 -p 8502:8502 -p 8503:8503 \
  --name comp40771-api-sandbox \
  pedrombmachado/comp40771-apisandbox:latest
```

---

## 4. Running the Evaluation

1. Open browser at: **http://localhost:8081/lab**
2. Open the notebook:  
   `COMP40771-CI-CWK-template_Somtochukwu_Osigwe-Daniel_N1419979.ipynb`
3. Click **Run → Run All Cells**

**Expected output from Section 16:**
- All 50 mystery API scenarios evaluated
- Score range: 1.10 (benign) to 7.53 (harmful)
- Label distribution: 34 × MEDIUM/RESTRICT, 16 × LOW/CONTINUE
- 100% agreement with sandbox ground truth

---

## 5. Project Structure
```
/opt/data/cwk/
├── COMP40771-CI-CWK-template_Somtochukwu_Osigwe-Daniel_N1419979.ipynb
├── docker-compose.yml
├── README.md
├── config/
│   ├── default.json        # default scoring weights
│   └── strict.json         # elevated-risk configuration
├── src/
│   ├── static_analysis.py  # AST parser and feature extractor
│   ├── risk.py             # weighted risk scoring engine
│   ├── sandbox.py          # Docker sandbox wrapper
│   ├── telemetry.py        # runtime telemetry capture
│   ├── report.py           # explainable report generator
│   ├── agents.py           # multi-agent orchestrator
│   ├── ga_probes.py        # Genetic Algorithm probe selection
│   ├── pso_config.py       # PSO configuration tuning
│   ├── rl_probe.py         # RL probe policy (Q-learning)
│   ├── mongo_store.py      # MongoDB report persistence
│   └── mqtt_publish.py     # MQTT risk alert publisher
├── workspace/              # mystery scripts evaluated by harness
├── outputs/                # generated risk reports (.txt)
└── logs/                   # telemetry JSON logs
```

---

## 6. Dependencies

All dependencies are installed inside the container via the Dockerfile.  
Key libraries: `requests`, `pandas`, `pymongo`, `paho-mqtt`, `scipy`, `numpy`

To manually verify inside the container:
```bash
pip list | grep -E "requests|pandas|pymongo|paho|scipy"
```

---

## 7. Requirements Coverage

| Req | Description | Location |
|---|---|---|
| 1 | Threat model | Section 1 markdown |
| 2 | Static analysis | Section 2, src/static_analysis.py |
| 3 | Risk scoring | Section 3, src/risk.py |
| 4 | Sandbox execution | Section 4, src/sandbox.py |
| 5 | Dynamic telemetry | Section 5, src/telemetry.py |
| 6 | GA probes | Section 6, src/ga_probes.py |
| 7 | PSO config | Section 7, src/pso_config.py |
| 8 | RL policy | Section 8, src/rl_probe.py |
| 9 | Multi-agent | Section 9, src/agents.py |
| 10 | Canary secrets | Section 10 |
| 11 | Adversarial (ART-11) | Section 11 |
| 12 | Explainable report | Section 12, src/report.py |
| 13 | JSON config | Section 0, config/ |
| 14 | Docker Compose + MQTT | docker-compose.yml, src/mqtt_publish.py |
| 15 | Ethics | Section 15 markdown |
| 16 | CWK mystery evaluation | Section 16 — all 50 APIs |
