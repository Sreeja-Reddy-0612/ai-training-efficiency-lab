from pydantic import BaseModel
from typing import List


class Benchmark(BaseModel):
    experiment_id: str
    model: str
    batch_size: int
    epochs: int
    throughput_samples_per_sec: float
    total_time_seconds: float
    peak_memory_gb: float
    device: str


class BenchmarkHistory(BaseModel):
    history: List[Benchmark]
