from app.model.searchers.abstract_substring_searcher import \
    AbstractSubstringSearcher


class BruteForceSearcher(AbstractSubstringSearcher):
    """Класс для алгоритма Брутфорс"""

    def search(self, string: str, substring: str) -> list[int]:
        str_len = len(string)
        substr_len = len(substring)
        if str_len == 0 or substr_len == 0 or str_len < substr_len:
            return []
        indexes = []
        for start_index in range(str_len - substr_len + 1):
            substring_found = True
            for i in range(substr_len):
                if string[start_index + i] != substring[i]:
                    substring_found = False
                    break
            if substring_found:
                indexes.append(start_index)
        return indexes
