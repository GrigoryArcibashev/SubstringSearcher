import tracemalloc
from contextlib import contextmanager
from typing import Optional


class MemoryProfiler:
    """Класс профилировщика памяти"""

    def __init__(self):
        self._peak: Optional[int] = None

    @contextmanager
    def profile(self):
        """Замеряет пик использования памяти"""
        tracemalloc.start()
        yield
        self._peak = tracemalloc.get_traced_memory()[-1]
        tracemalloc.reset_peak()
        tracemalloc.stop()

    def get_peak_expended_memory_in_bytes(self) -> int:
        """
        Возвращает максимальное количество байт,
        задействованное во время работы профилировщика
        """
        if self._peak is None:
            raise Exception('Profiler has not started yet')
        return self._peak
