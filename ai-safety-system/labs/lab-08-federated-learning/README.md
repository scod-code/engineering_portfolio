# Lab 8 — Federated Learning Optimisation and Adversarial Robustness

Two-part lab covering distributed ML optimisation and adversarial robustness testing.

## Part A — Bayesian Optimisation for Secure Federated Learning
- 12-client federated simulation with non-IID data
- FGSM adversarial training and sign-flip poisoning resistance
- Optuna TPE Bayesian optimisation across 5-dimensional config space
- Best composite objective score: 0.9947 across 30 trials

## Part B — ART-11-SIM Adversarial Robustness Simulator
- Four perturbation scenarios: Malformed Inputs, Missing Files,
  Randomised Filenames, Timeout Constraints
- Three behavioural profiles: Benign Baseline, Unsafe, Fragile

## Key Skills
Python, PyTorch, Optuna (TPE), federated learning, FGSM adversarial training,
trimmed mean aggregation, telemetry simulation, seed-controlled reproducibility

## Files
- `lab08-federated-learning.ipynb` — Lab notebook
- `lab-guide.pdf` — Lab instructions
