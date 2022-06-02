from app.model.searchers.abstract_substring_searcher import \
    AbstractSubstringSearcher


class RabinKarpWithPolynomialHashSearcher(AbstractSubstringSearcher):
    """Класс для алгоритма Рабина-Карпа с полиномиальным хэшем"""

    def __init__(self):
        self._Q: int = 1046527
        self._R: int = 1200

    def search(self, string: str, substring: str) -> list[int]:
        N = len(string)
        M = len(substring)
        if N == 0 or M == 0 or N < M:
            return []
        indexes = []
        str_hash = self._hash(string, M)
        substr_hash = self._hash(substring, M)
        if str_hash == substr_hash:
            indexes.append(0)
        RM = self._calculate_RM(M)
        for i in range(M, N):
            str_hash = (
                               str_hash + self._Q - RM * ord(
                               string[i - M]) % self._Q
                       ) % self._Q
            str_hash = (str_hash * self._R + ord(string[i])) % self._Q
            if str_hash == substr_hash:
                if self._compare(string, substring, i - M + 1):
                    indexes.append(i - M + 1)
        return indexes

    def _hash(self, string: str, length: int) -> int:
        """
        Возвращает хэш для строки

        :param string: строка, для которой вычисляется хэш
        :param length: количество символов строки (начиная с 0),
        которые используются для хэширования
        :return: хэш
        """
        h = 0
        for i in range(length):
            h = (self._R * h + ord(string[i])) % self._Q
        return h

    def _calculate_RM(self, M: int) -> int:
        """Возвращает self._R ^ (M-1) % self._Q"""
        RM = 1
        for _ in range(0, M - 1):
            RM = (self._R * RM) % self._Q
        return RM

    @staticmethod
    def _compare(string: str, substring: str, start_index: int) -> bool:
        """
        Сравнивает строку substring со строкой string,
        начиная с индекса start_index

        :param start_index: индекс для строки string,
        с которого начинается сравнение
        :return: строки совпали -> True, иначе -> False
        """
        for i in range(len(substring)):
            if string[start_index + i] != substring[i]:
                return False
        return True
