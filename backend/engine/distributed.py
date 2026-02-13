import os
import torch
import torch.distributed as dist


def init_distributed():
    """
    Initialize distributed training environment.
    """

    if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
        rank = int(os.environ["RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
        local_rank = int(os.environ["LOCAL_RANK"])

        dist.init_process_group(backend="nccl" if torch.cuda.is_available() else "gloo")

        torch.cuda.set_device(local_rank) if torch.cuda.is_available() else None

        return True, rank, world_size, local_rank
    else:
        return False, 0, 1, 0


def cleanup_distributed():
    if dist.is_initialized():
        dist.destroy_process_group()
