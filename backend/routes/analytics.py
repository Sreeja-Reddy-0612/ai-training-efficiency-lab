from fastapi import APIRouter
import json
import os

router = APIRouter()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_DIR = os.path.join(BASE_DIR, "results")


@router.get("/summary")
def get_summary():
    file_path = os.path.join(RESULTS_DIR, "phase6_latest.json")

    if not os.path.exists(file_path):
        return {"error": "No summary available"}

    with open(file_path, "r") as f:
        data = json.load(f)

    return {
        "experiment_id": data.get("experiment_id"),
        "device": data.get("device"),
        "throughput": data.get("throughput_samples_per_sec"),
        "total_time": data.get("total_time_seconds"),
        "mixed_precision": data.get("mixed_precision"),
        "distributed": data.get("distributed"),
    }
