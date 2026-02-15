from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict to localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")


@app.get("/")
def root():
    return {"message": "AI Training Efficiency API Running 🚀"}


@app.get("/latest")
def get_latest_result():
    file_path = os.path.join(RESULTS_DIR, "phase6_latest.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    return {"error": "No latest result found"}


@app.get("/history")
def get_history():
    file_path = os.path.join(RESULTS_DIR, "benchmark_history.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    return []
