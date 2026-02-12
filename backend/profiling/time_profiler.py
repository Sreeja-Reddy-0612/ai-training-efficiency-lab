import time

class TimeProfiler:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    def get_elapsed_time(self):
        return self.end_time - self.start_time
