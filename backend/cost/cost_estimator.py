from backend.cost.gpu_pricing import GPU_PRICING


def estimate_cost(device, total_time_seconds):
    """
    Estimate training cost based on device and execution time.
    """

    hourly_rate = GPU_PRICING.get(device, GPU_PRICING["cpu"])
    hours = total_time_seconds / 3600

    cost = hours * hourly_rate

    return round(cost, 4)
