# Phase 7 Architecture

Backend
--------
Training Engine (PyTorch + HF)
Profiler (Time + Memory)
Cost Engine
Distributed Engine
Analytics Engine

↓ Saves JSON

Frontend
--------
Reads sampleData.json
Displays:

- Best Experiment
- Throughput Chart
- Cost Chart
- Benchmark Table
- Decision Intelligence Panel

Architecture Flow:

Training → Metrics → JSON → Dashboard → Insights
