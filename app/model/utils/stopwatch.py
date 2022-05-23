import time
from typing import Optional


class Stopwatch:
    def __init__(self):
        self._start: Optional[float] = None
        self._time: Optional[float] = None

    def start(self) -> None:
        if self._start is not None:
            raise Exception("Stopwatch has already been started")
        self._start = time.time()
        self._time = None

    def stop(self) -> None:
        if self._start is None:
            raise Exception("Stopwatch has not started yet")
        if self._time is not None:
            raise Exception("Stopwatch has already been stopped")
        self._time = time.time() - self._start
        self._start = None

    def get_time_in_seconds(self) -> float:
        if self._time is not None:
            return self._time
        if self._start is None:
            raise Exception("Stopwatch has not started yet")
        raise Exception("Stopwatch is not stopped yet")
