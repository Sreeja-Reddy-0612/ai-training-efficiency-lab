import torch
import argparse
import os
import json
from torch.utils.data import DataLoader
from torch.optim import AdamW
from transformers import get_scheduler
from datasets import load_dataset
from datetime import datetime
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler

from engine.config_loader import load_config
from engine.model_loader import load_model_and_tokenizer
from engine.registry import save_benchmark_result
from engine.analyzer import analyze_benchmarks
from engine.distributed import init_distributed, cleanup_distributed
from profiling.memory_profiler import get_peak_memory, reset_memory_stats
from profiling.time_profiler import TimeProfiler
from profiling.throughput import calculate_throughput


# ------------------------------------------------
# CLI Arguments
# ------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="configs/baseline_config.json")
parser.add_argument("--batch_size", type=int, default=None)
parser.add_argument("--epochs", type=int, default=None)
parser.add_argument("--mixed_precision", action="store_true")
parser.add_argument("--analyze", action="store_true")
parser.add_argument("--cost_device", type=str, default="cpu")
parser.add_argument("--distributed", action="store_true")

args = parser.parse_args()

# ------------------------------------------------
# Initialize Distributed Training
# ------------------------------------------------
is_distributed = False
rank = 0
world_size = 1
local_rank = 0

if args.distributed:
    is_distributed, rank, world_size, local_rank = init_distributed()

# ------------------------------------------------
# Analytics-Only Mode
# ------------------------------------------------
if args.analyze:
    report = analyze_benchmarks(device_for_cost=args.cost_device)
    print("Benchmark Analysis Report:")
    print(json.dumps(report, indent=4))
    exit()

# ------------------------------------------------
# Load Config
# ------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, args.config)

config = load_config(CONFIG_PATH)

if args.batch_size:
    config["batch_size"] = args.batch_size

if args.epochs:
    config["epochs"] = args.epochs

# ------------------------------------------------
# Device Setup
# ------------------------------------------------
if torch.cuda.is_available():
    DEVICE = torch.device(f"cuda:{local_rank}")
else:
    DEVICE = torch.device("cpu")

# ------------------------------------------------
# Model & Tokenizer
# ------------------------------------------------
model, tokenizer = load_model_and_tokenizer(config["model_name"])
model.to(DEVICE)

if is_distributed:
    model = DDP(
        model,
        device_ids=[local_rank] if torch.cuda.is_available() else None
    )

# ------------------------------------------------
# Dataset
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
dataset = dataset.rename_column("label", "labels")
dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "labels"]
)

if is_distributed:
    sampler = DistributedSampler(dataset)
    dataloader = DataLoader(
        dataset,
        batch_size=config["batch_size"],
        sampler=sampler
    )
else:
    dataloader = DataLoader(
        dataset,
        batch_size=config["batch_size"]
    )

# ------------------------------------------------
# Optimizer & Scheduler
# ------------------------------------------------
optimizer = AdamW(model.parameters(), lr=config["learning_rate"])
num_training_steps = len(dataloader) * config["epochs"]

scheduler = get_scheduler(
    "linear",
    optimizer=optimizer,
    num_warmup_steps=0,
    num_training_steps=num_training_steps,
)

# ------------------------------------------------
# Profiling Setup
# ------------------------------------------------
time_profiler = TimeProfiler()
reset_memory_stats()

scaler = None
if args.mixed_precision and torch.cuda.is_available():
    scaler = torch.cuda.amp.GradScaler()

# ------------------------------------------------
# Training Loop
# ------------------------------------------------
model.train()
time_profiler.start()

total_samples = 0

for epoch in range(config["epochs"]):

    if is_distributed:
        sampler.set_epoch(epoch)

    for batch in dataloader:
        batch = {k: v.to(DEVICE) for k, v in batch.items()}

        optimizer.zero_grad()

        if scaler:
            with torch.cuda.amp.autocast():
                outputs = model(**batch)
                loss = outputs.loss

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

        scheduler.step()
        total_samples += batch["input_ids"].size(0)

time_profiler.stop()

# ------------------------------------------------
# Collect Metrics
# ------------------------------------------------
total_time = time_profiler.get_elapsed_time()
peak_memory = get_peak_memory()
throughput = calculate_throughput(total_samples, total_time)

experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")

results = {
    "experiment_id": experiment_id,
    "mode": "transformer_baseline_distributed" if is_distributed else "transformer_baseline",
    "model": config["model_name"],
    "batch_size": config["batch_size"],
    "epochs": config["epochs"],
    "mixed_precision": args.mixed_precision,
    "total_time_seconds": round(total_time, 4),
    "peak_memory_gb": round(peak_memory, 4),
    "throughput_samples_per_sec": round(throughput, 2),
    "device": str(DEVICE),   # FIXED
    "distributed": is_distributed,
    "world_size": world_size
}

# ------------------------------------------------
# Save Results (Rank 0 Only)
# ------------------------------------------------
if rank == 0:
    os.makedirs("results", exist_ok=True)

    with open("results/phase6_latest.json", "w") as f:
        json.dump(results, f, indent=4)

    save_benchmark_result(results)

    print("Phase 6 Benchmark Completed.")
    print(json.dumps(results, indent=4))

# ------------------------------------------------
# Cleanup
# ------------------------------------------------
if is_distributed:
    cleanup_distributed()
