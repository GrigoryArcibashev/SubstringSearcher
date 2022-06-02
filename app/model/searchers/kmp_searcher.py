from app.model.searchers.abstract_substring_searcher import \
    AbstractSubstringSearcher


class KMPSearcher(AbstractSubstringSearcher):
    """Класс для алгоритма Кнута — Морриса — Пратта"""

    def search(self, string: str, substring: str) -> list[int]:
        str_len = len(string)
        substr_len = len(substring)
        if str_len == 0 or substr_len == 0 or str_len < substr_len:
            return []
        indexes = []
        substring_borders = KMPSearcher._find_borders(substring)
        compare_index = 0
        for i in range(str_len):
            while compare_index and string[i] != substring[compare_index]:
                compare_index = substring_borders[compare_index - 1]
            if string[i] == substring[compare_index]:
                compare_index += 1
            if compare_index == substr_len:
                indexes.append(i - compare_index + 1)
                compare_index = substring_borders[substr_len - 1]
        return indexes

    @staticmethod
    def _find_borders(string: str) -> list[int]:
        """Составляет список значений префикс-функции для строки"""
        borders = [0] * len(string)
        current_index = 0
        for i in range(1, len(string)):
            while current_index and string[current_index] != string[i]:
                current_index = borders[current_index - 1]
            if string[current_index] == string[i]:
                current_index += 1
            borders[i] = current_index
        return borders
