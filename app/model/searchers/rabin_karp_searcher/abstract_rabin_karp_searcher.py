from abc import abstractmethod

from memory_profiler import profile

from app.model.searchers.abstract_substring_searcher import AbstractSubstringSearcher
from app.model.utils.stopwatch_decorator import stopwatch


class AbstractRabinKarpSearcher(AbstractSubstringSearcher):
    @stopwatch()
    @profile
    def search(self, string: str, substring: str) -> list[int]:
        indexes = []
        str_hash = self._get_hash(
                string,
                len(substring))
        substr_hash = self._get_hash(
                substring,
                len(substring))
        for i in range(len(string) - len(substring)):
            if str_hash == substr_hash:
                if self._compare(string, substring, i):
                    indexes.append(i)
            str_hash = self._get_updated_hash(
                    str_hash,
                    string,
                    i,
                    len(substring))
        return indexes

    @abstractmethod
    def _get_hash(self, string: str, max_power: int) -> int:
        pass

    @abstractmethod
    def _get_updated_hash(
            self,
            hash: int,
            string: str,
            index_of_first_char: int,
            max_power: int) -> int:
        pass

    @staticmethod
    def _compare(string: str, substring: str, start_index: int) -> bool:
        for shift in range(len(substring)):
            if string[start_index + shift] != substring[shift]:
                return False
        return True
