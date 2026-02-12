import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
import json
import os

from profiling.memory_profiler import get_peak_memory, reset_memory_stats
from profiling.time_profiler import TimeProfiler
from profiling.throughput import calculate_throughput

# -----------------------------
# 1. Configuration
# -----------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 32
EPOCHS = 2
INPUT_DIM = 768
NUM_SAMPLES = 5000

# -----------------------------
# 2. Dummy Dataset
# -----------------------------
X = torch.randn(NUM_SAMPLES, INPUT_DIM)
y = torch.randint(0, 2, (NUM_SAMPLES,))

dataset = TensorDataset(X, y)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# -----------------------------
# 3. Simple Model
# -----------------------------
model = nn.Sequential(
    nn.Linear(INPUT_DIM, 512),
    nn.ReLU(),
    nn.Linear(512, 2)
).to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# -----------------------------
# 4. Profiling Setup
# -----------------------------
time_profiler = TimeProfiler()
reset_memory_stats()

# -----------------------------
# 5. Training Loop
# -----------------------------
model.train()
time_profiler.start()

total_samples_processed = 0

for epoch in range(EPOCHS):
    for batch_X, batch_y in dataloader:
        batch_X = batch_X.to(DEVICE)
        batch_y = batch_y.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

        total_samples_processed += batch_X.size(0)

time_profiler.stop()

# -----------------------------
# 6. Metrics Collection
# -----------------------------
total_time = time_profiler.get_elapsed_time()
peak_memory = get_peak_memory()
throughput = calculate_throughput(total_samples_processed, total_time)

results = {
    "mode": "single_gpu_fp32_baseline",
    "epochs": EPOCHS,
    "total_time_seconds": round(total_time, 4),
    "peak_memory_gb": round(peak_memory, 4),
    "throughput_samples_per_sec": round(throughput, 2),
    "device": DEVICE
}

# -----------------------------
# 7. Save Results
# -----------------------------
os.makedirs("../results", exist_ok=True)

with open("../results/phase1_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("Benchmark Completed.")
print(json.dumps(results, indent=4))
