from abstract_substring_searcher import AbstractSubstringSearcher


class BoyerMooreSearcher(AbstractSubstringSearcher):
    def search(self, string: str, substring: str) -> list[int]:
        indexes = []
        str_len = len(string)
        substr_len = len(substring)
        badChar = self.badCharHeuristic(substring, substr_len)
        shift = 0
        while shift <= str_len - substr_len:
            j = substr_len - 1
            while j >= 0 and substring[j] == string[shift + j]:
                j -= 1
            if j < 0:
                indexes.append(shift)
                if shift + substr_len < str_len:
                    shift += substr_len - badChar.get(
                            ord(string[shift + substr_len]),
                            -1)
                else:
                    shift += 1
            else:
                shift += max(1, j - badChar.get(ord(string[shift + j]), -1))
        return indexes

    @staticmethod
    def badCharHeuristic(string: str, size: int):
        badChar = dict()
        for i in range(size):
            badChar[ord(string[i])] = i
        return badChar