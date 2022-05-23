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

    @property
    def peak_expended_memory_in_bytes(self) -> int:
        return self._peak
