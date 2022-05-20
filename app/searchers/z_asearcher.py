from memory_profiler import profile

from app.searchers.abstract_substring_searcher import AbstractSubstringSearcher
from app.stopwatch_decorator import stopwatch


class ZSearcher(AbstractSubstringSearcher):
    @stopwatch()
    @profile
    def search(self, string: str, substring: str) -> list[int]:
        indexes = []
        concat = substring + "$" + string
        length = len(concat)
        z = [0] * length
        self.get_z_array(concat, z)
        for i in range(length):
            if z[i] == len(substring):
                indexes.append(i - len(substring) - 1)
        return indexes

    @staticmethod
    def get_z_array(string, z):
        n = len(string)
        length, r, k = 0, 0, 0
        for i in range(1, n):
            if i > r:
                length, r = i, i
                while r < n and string[r - length] == string[r]:
                    r += 1
                z[i] = r - length
                r -= 1
            else:
                k = i - length
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    length = i
                    while r < n and string[r - length] == string[r]:
                        r += 1
                    z[i] = r - length
                    r -= 1
