import tracemalloc
from contextlib import contextmanager
from typing import Optional


class MemoryProfiler:
    def __init__(self):
        self._peak: Optional[int] = None

    @contextmanager
    def profile(self):
        tracemalloc.start()
        yield
        self._peak = tracemalloc.get_traced_memory()[-1]
        tracemalloc.reset_peak()
        tracemalloc.stop()

    def get_peak_expended_memory_in_bytes(self) -> int:
        if self._peak is None:
            raise Exception("Profiler has not started yet")
        return self._peak
