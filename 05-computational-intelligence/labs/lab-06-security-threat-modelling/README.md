# Lab 6 — Threat Modelling, Zero-Trust Security, and Runtime Telemetry

Approached code security from a zero-trust perspective — treating all code
as untrusted by default. Built threat models, static analysis tools, and
runtime process telemetry.

## Key Work
- Formal threat model for a code-ingestion microservice
- AST-based static analysis detecting eval, exec, subprocess, network imports
- Runtime telemetry using psutil: CPU, memory, file handles during execution
- Secret exposure detection via environment variable scanning
- Command injection demonstration and dependency risk inspection

## Key Skills
Python, psutil, AST, zero-trust security, threat modelling,
dependency auditing, runtime telemetry, containerisation

## Files
- `lab06-security-threat-modelling.ipynb` — Lab notebook
- `lab-guide.pdf` — Lab instructions
- `lecture-notes.pdf` — Containerisation and Distributed Technologies slides
- `lab-files/` — Supporting lab files
