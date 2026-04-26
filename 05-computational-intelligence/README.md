# Computational Intelligence — COMP40771

**MSc Robotics and Intelligent Systems** | Nottingham Trent University | 2025–26

This module covered nature-inspired optimisation, reinforcement learning, signal
processing, multi-agent systems, MLOps, and AI safety engineering. Work spanned
ten labs and an independently assessed capstone project.

---

## Repository Contents

| Item | Description |
|------|-------------|
| `src/` | All Python source modules for the capstone safety harness |
| `config/` | JSON configuration files for sandbox limits and scoring weights |
| `docker-compose.yml` | Multi-container stack — JupyterLab, MQTT broker, orchestrator |
| `mosquitto.conf` | Eclipse Mosquitto MQTT broker configuration |
| `Jenkinsfile` | Declarative CI/CD pipeline (Checkout, Install, Test, Report, MQTT) |
| `requirements.txt` | Frozen Python dependencies for reproducibility |

---

## Module Projects

### Lab 2 — Continuous Optimisation and Hyperparameter Tuning
Implemented and benchmarked five nature-inspired optimisation algorithms: PSO,
CMA-ES, NES, Differential Evolution, and Artificial Bee Colony. Applied to nonlinear
regression and neural network hyperparameter search, with performance compared
against linear regression baselines.

### Lab 3 — Ecosystem Stability Optimisation with Evolutionary Algorithms
Designed a multi-parameter optimisation problem: finding initial conditions for a
three-species predator-prey-resource simulation that maintained stable coexistence
across 100 stochastic steps. Implemented and compared Evolution Strategy (ES) and
Genetic Algorithm (GA) using median-over-seeds evaluation to control for stochasticity.

### Lab 4 — EEG Brain-Signal Feature Engineering and Classification
Built a full signal processing and classification pipeline on 36-subject EEG data.
Stages included Butterworth bandpass filtering, 50 Hz notch filtering, 1-second window
segmentation, and extraction of 247 features per window (Hjorth parameters, spectral
band powers via Welch PSD, STFT summaries). Achieved 95.1% balanced accuracy using
Random Forest feature selection with Logistic Regression.

### Lab 5 — Reinforcement Learning Agent Design and Evaluation
Implemented five RL algorithms from scratch on a custom 5x5 Gridworld MDP:
First-Visit Monte Carlo, TD(0), Q-Learning, SARSA, and linear function approximation
with semi-gradient Q-learning. Compared sample efficiency, stability, and learned
policy quality across all methods.

### Lab 6 — Threat Modelling, Zero-Trust Security, and Runtime Telemetry
Built a formal threat model for a code-ingestion microservice, implemented AST-based
static analysis to detect dangerous primitives before execution, and developed runtime
process telemetry using psutil — capturing CPU, memory, and file handle counts during
live sandboxed execution.

### Lab 8 — Federated Learning Optimisation and Adversarial Robustness
Part A: 12-client federated learning simulation with non-IID data, FGSM adversarial
training, and sign-flip poisoning resistance. Used Optuna TPE Bayesian optimisation
across a 5-dimensional config space, achieving composite objective score 0.9947.
Part B: ART-11-SIM telemetry simulator modelling four adversarial perturbation
scenarios across three behavioural profiles for robustness testing.

### Lab 9 — MLOps: CI/CD Pipeline with Jenkins, Gitea, MQTT, and LLM Integration
Converted the Lab 8 simulator into a structured Python project and routed it through
a full CI/CD pipeline. Used Jenkins with a declarative Groovy Jenkinsfile, Gitea for
version control, pytest for automated testing, Ollama-hosted LLMs to auto-generate
improved code variants, and MQTT for real-time build result broadcasting.
Achieved BUILD SUCCESS with 9/9 tests passing across original and LLM-generated files.

### Lab 10 — Zero-Trust Behavioural Monitoring: Architecture and Systems Integration
Deployed a five-container Docker Compose environment (sandbox, monitor, Ollama,
MongoDB, development workspace) and implemented the full investigation workflow:
telemetry collection across six endpoints, risk scoring with weighted severity levels,
structured report generation, MongoDB audit persistence, and Ollama LLM reasoning.

### Capstone Coursework — Adaptive Code Safety Harness
Independently designed and implemented an explainable zero-trust AI code evaluation
system graded against 15 requirements across Pass, Commendation, and Distinction tiers.
See `src/` for full source code. The assessed Jupyter notebook remains in the private
NTU Olympus repository.

---

## Source Module Reference

| File | Purpose |
|------|---------|
| `src/static_analysis.py` | AST parser — flags eval, exec, subprocess, network imports |
| `src/risk.py` | Quantitative risk scoring engine combining static and dynamic signals |
| `src/sandbox.py` | Docker-based sandboxed execution wrapper with canary deception |
| `src/telemetry.py` | Runtime telemetry collection via psutil and lsof |
| `src/report.py` | Markdown risk report generation with evidence-linked explanations |
| `src/ga_probes.py` | Genetic Algorithm probe generator — evolves inputs to maximise risk signals |
| `src/pso_config.py` | PSO configuration search — finds least-privilege sandbox settings |
| `src/rl_probe.py` | Q-learning probe selection agent with 12-state space |
| `src/agents.py` | Multi-agent orchestrator — filesystem, network, process, resource agents |
| `src/mongo_store.py` | MongoDB audit trail persistence with graceful fallback |
| `src/mqtt_publish.py` | MQTT publisher — broadcasts risk results to broker topic |
| `src/original_art11_sim.py` | ART-11-SIM adversarial robustness simulator (Lab 8 origin) |

---

## Skills Demonstrated

**Languages:** Python, Groovy (Jenkinsfile)  
**ML/AI:** Reinforcement Learning, Genetic Algorithms, PSO, Bayesian Optimisation (Optuna),
Federated Learning, EEG signal processing, feature engineering, scikit-learn  
**MLOps:** Jenkins CI/CD, Docker Compose, Gitea, MQTT, pytest, JUnit XML, Ollama (local LLM)  
**Security:** Zero-trust architecture, AST static analysis, runtime telemetry, threat modelling,
sandboxed execution, canary deception, explainable AI  
**Data Engineering:** MongoDB, structured audit logging, REST API design and consumption  
**Tools:** Jupyter Notebooks, Git, psutil, paho-mqtt, pymongo
