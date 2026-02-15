from fastapi import APIRouter
import json
import os

router = APIRouter()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_DIR = os.path.join(BASE_DIR, "results")


@router.get("/latest")
def get_latest():
    file_path = os.path.join(RESULTS_DIR, "phase6_latest.json")

    if not os.path.exists(file_path):
        return {"error": "No latest benchmark found"}

    with open(file_path, "r") as f:
        return json.load(f)


@router.get("/history")
def get_history():
    file_path = os.path.join(RESULTS_DIR, "benchmark_history.json")

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as f:
        return json.load(f)
