# Phase 8 – API Snapshot

## Swagger URL
http://127.0.0.1:8000/docs

---

## Available Endpoints

GET /benchmarks/latest  
Returns latest experiment

GET /benchmarks/history  
Returns all benchmark history

GET /analytics/summary  
Returns:
- Recommended experiment
- GPU speedup
- Optimization insight

---

## Example Analytics Output

{
  "recommended_experiment": "20260213_051045",
  "device": "cuda:0",
  "throughput": 124.12,
  "gpu_speedup_vs_cpu": 49.72,
  "optimization_insight": "Mixed precision improves performance significantly."
}
