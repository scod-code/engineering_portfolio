# config — Configuration Files

All system hyperparameters are defined here as JSON — no magic numbers in source code.

| File | Sandbox Limits | Scoring Weights | Use Case |
|------|---------------|-----------------|----------|
| `default.json` | 256MB memory, 0.5 CPU, 30s timeout | Standard weights | Normal evaluation |
| `strict.json` | 128MB memory, 0.25 CPU, 15s timeout | Higher weights | High-risk environments |

Swapping config files changes risk tolerance without touching source code,
demonstrating config-driven system design.
