import torch

def get_peak_memory():
    """
    Returns peak GPU memory allocated (in GB).
    If CUDA not available, returns 0.
    """
    if torch.cuda.is_available():
        peak_memory = torch.cuda.max_memory_allocated()
        return peak_memory / (1024 ** 3)  # Convert bytes to GB
    else:
        return 0.0


def reset_memory_stats():
    """
    Resets GPU memory tracking if CUDA is available.
    """
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
