import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from datasets import load_dataset
import json
import os

from engine.config_loader import load_config
from engine.model_loader import load_model_and_tokenizer
from profiling.memory_profiler import get_peak_memory, reset_memory_stats
from profiling.time_profiler import TimeProfiler
from profiling.throughput import calculate_throughput

# ------------------------------------------------
# 1. Load Config
# ------------------------------------------------
config = load_config("configs/baseline_config.json")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ------------------------------------------------
# 2. Load Model & Tokenizer
# ------------------------------------------------
model, tokenizer = load_model_and_tokenizer(config["model_name"])
model.to(DEVICE)

# ------------------------------------------------
# 3. Load Dataset (Small Subset)
# ------------------------------------------------
dataset = load_dataset("imdb", split="train[:1%]")

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=config["max_length"]
    )

dataset = dataset.map(tokenize_function, batched=True)
# dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
dataset = dataset.rename_column("label", "labels")
dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

dataloader = DataLoader(dataset, batch_size=config["batch_size"])

# ------------------------------------------------
# 4. Optimizer
# ------------------------------------------------
optimizer = AdamW(model.parameters(), lr=config["learning_rate"])

# ------------------------------------------------
# 5. Profiling Setup
# ------------------------------------------------
time_profiler = TimeProfiler()
reset_memory_stats()

# ------------------------------------------------
# 6. Training Loop
# ------------------------------------------------
model.train()
time_profiler.start()

total_samples = 0

for epoch in range(config["epochs"]):
    for batch in dataloader:
        batch = {k: v.to(DEVICE) for k, v in batch.items()}

        outputs = model(**batch)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_samples += batch["input_ids"].size(0)

time_profiler.stop()

# ------------------------------------------------
# 7. Collect Metrics
# ------------------------------------------------
total_time = time_profiler.get_elapsed_time()
peak_memory = get_peak_memory()
throughput = calculate_throughput(total_samples, total_time)

results = {
    "mode": "transformer_baseline",
    "model": config["model_name"],
    "epochs": config["epochs"],
    "total_time_seconds": round(total_time, 4),
    "peak_memory_gb": round(peak_memory, 4),
    "throughput_samples_per_sec": round(throughput, 2),
    "device": DEVICE
}

# ------------------------------------------------
# 8. Save Results
# ------------------------------------------------
os.makedirs("results", exist_ok=True)

with open("results/phase2_results.json", "w") as f:
    json.dump(results, f, indent=4)

print("Phase 2 Benchmark Completed.")
print(json.dumps(results, indent=4))
