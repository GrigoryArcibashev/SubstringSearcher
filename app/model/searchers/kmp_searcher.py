from memory_profiler import profile

from app.model.searchers.abstract_substring_searcher import AbstractSubstringSearcher
from app.model.utils.stopwatch_decorator import stopwatch


class KMPSearcher(AbstractSubstringSearcher):
    @stopwatch()
    @profile
    def search(self, string: str, substring: str) -> list[int]:
        indexes = []
        substring_borders = KMPSearcher._find_borders(substring)
        compare_index = 0
        for i in range(len(string)):
            while compare_index and string[i] != substring[compare_index]:
                compare_index = substring_borders[compare_index - 1]
            if string[i] == substring[compare_index]:
                compare_index += 1
            if compare_index == len(substring):
                indexes.append(i - compare_index + 1)
                compare_index = substring_borders[len(substring) - 1]
        return indexes

    @staticmethod
    def _find_borders(substring: str) -> list[int]:
        borders = [0] * len(substring)
        current_index = 0
        for i in range(1, len(substring)):
            while current_index and substring[current_index] != substring[i]:
                current_index = borders[current_index - 1]
            if substring[current_index] == substring[i]:
                current_index += 1
            borders[i] = current_index
        return borders
