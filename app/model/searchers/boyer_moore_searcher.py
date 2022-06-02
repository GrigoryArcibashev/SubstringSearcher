from app.model.searchers.abstract_substring_searcher import \
    AbstractSubstringSearcher


class BoyerMooreSearcher(AbstractSubstringSearcher):
    """Класс для алгоритма Бойера-Мура"""

    def search(self, string: str, substring: str) -> list[int]:
        str_len = len(string)
        substr_len = len(substring)
        if str_len == 0 or substr_len == 0 or str_len < substr_len:
            return []
        indexes = []
        badChar = self._bad_char_heuristic(substring)
        shift = 0
        while shift <= str_len - substr_len:
            j = substr_len - 1
            while j >= 0 and substring[j] == string[shift + j]:
                j -= 1
            if j < 0:
                indexes.append(shift)
                if shift + substr_len < str_len:
                    shift += substr_len - badChar.get(
                        ord(string[shift + substr_len]), -1
                    )
                else:
                    shift += 1
            else:
                shift += max(1, j - badChar.get(ord(string[shift + j]), -1))
        return indexes

    @staticmethod
    def _bad_char_heuristic(string: str) -> dict[int, int]:
        """Вычисляет эвристику плохого символа для строки"""
        badChar = dict()
        for i in range(len(string)):
            badChar[ord(string[i])] = i
        return badChar
