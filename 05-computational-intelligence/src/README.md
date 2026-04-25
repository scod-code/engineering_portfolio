# src — Source Modules

Core Python modules for the Adaptive Code Safety Harness (COMP40771 Capstone).

Each module is independently importable and handles one layer of the analysis pipeline.

| Module | Layer | Key Functions |
|--------|-------|---------------|
| `static_analysis.py` | Pre-execution | `extract_features()`, `analyse_file()` |
| `risk.py` | Scoring | `compute_risk()`, `classify_risk()`, `load_config()` |
| `sandbox.py` | Execution | `run_in_sandbox()`, `plant_canaries()`, `check_canary_access()` |
| `telemetry.py` | Monitoring | `monitor_process()`, `snapshot_network()`, `collect_telemetry_from_sandbox_result()` |
| `report.py` | Output | `generate_report()`, `generate_behavioral_report()` |
| `ga_probes.py` | Optimisation | `evolve_probes()`, `random_probe_baseline()` |
| `pso_config.py` | Optimisation | `pso_config_search()` |
| `rl_probe.py` | Optimisation | `train_rl_agent()`, `select_probe()` |
| `agents.py` | Multi-agent | `FilesystemAgent`, `NetworkAgent`, `ProcessAgent`, `ResourceAgent`, `Orchestrator` |
| `mongo_store.py` | Persistence | `store_run()`, `query_runs()` |
| `mqtt_publish.py` | Messaging | `publish_mqtt()` |
| `original_art11_sim.py` | Simulation | ART-11-SIM adversarial robustness simulator |
