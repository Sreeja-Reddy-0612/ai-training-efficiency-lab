import json
import os
from cost.cost_estimator import estimate_cost

HISTORY_FILE = "results/benchmark_history.json"
ANALYTICS_FILE = "results/analytics_report.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        raise FileNotFoundError("No benchmark history found.")

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def analyze_benchmarks(device_for_cost="cpu"):
    history = load_history()

    if len(history) == 0:
        return {"message": "No experiments available for analysis."}

    # Add cost to each experiment
    for exp in history:
        exp["estimated_cost"] = estimate_cost(
            device_for_cost,
            exp["total_time_seconds"]
        )

    # Rank by throughput
    ranked_by_throughput = sorted(
        history,
        key=lambda x: x["throughput_samples_per_sec"],
        reverse=True
    )

    # Rank by time
    ranked_by_time = sorted(
        history,
        key=lambda x: x["total_time_seconds"]
    )

    # Rank by cost (lowest first)
    ranked_by_cost = sorted(
        history,
        key=lambda x: x["estimated_cost"]
    )

    best_throughput = ranked_by_throughput[0]
    fastest_run = ranked_by_time[0]
    cheapest_run = ranked_by_cost[0]

    avg_throughput = sum(x["throughput_samples_per_sec"] for x in history) / len(history)
    avg_time = sum(x["total_time_seconds"] for x in history) / len(history)
    avg_cost = sum(x["estimated_cost"] for x in history) / len(history)

    report = {
        "total_experiments": len(history),
        "best_throughput_experiment": best_throughput,
        "fastest_experiment": fastest_run,
        "cheapest_experiment": cheapest_run,
        "average_throughput": round(avg_throughput, 4),
        "average_time_seconds": round(avg_time, 4),
        "average_cost": round(avg_cost, 4),
        "ranked_by_cost": ranked_by_cost
    }

    os.makedirs("results", exist_ok=True)

    with open(ANALYTICS_FILE, "w") as f:
        json.dump(report, f, indent=4)

    return report
