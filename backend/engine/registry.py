import os
import json

HISTORY_FILE = "results/benchmark_history.json"

def save_benchmark_result(result):
    os.makedirs("results", exist_ok=True)

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(result)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)
