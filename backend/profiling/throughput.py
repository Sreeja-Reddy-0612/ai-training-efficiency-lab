def calculate_throughput(total_samples, total_time):
    """
    samples per second
    """
    if total_time == 0:
        return 0
    return total_samples / total_time
