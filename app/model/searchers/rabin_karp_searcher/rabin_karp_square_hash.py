import math

from app.model.searchers.abstract_substring_searcher import AbstractSubstringSearcher


class RabinKarpWithSquareHashSearcher(AbstractSubstringSearcher):
    """Класс для алгоритма Рабина-Карпа с хэшем на сумме квадратов"""

    def __init__(self):
        self._Q: int = 1046527

    def search(self, string: str, substring: str) -> list[int]:
        indexes = []
        str_hash = self._hash(string, len(substring))
        substr_hash = self._hash(substring, len(substring))
        count_of_comparers = len(string) - len(substring) + 1
        for i in range(count_of_comparers):
            if str_hash == substr_hash:
                if self._compare(string, substring, i):
                    indexes.append(i)
            if i < count_of_comparers - 1:
                str_hash = self._get_updated_hash(str_hash, string, i, len(substring))
        return indexes

    def _hash(self, string: str, length: int) -> int:
        """
        Возвращает хэш для строки

        :param string: строка, для которой вычисляется хэш
        :param length: количество символов строки (начиная с 0), которые используются для хэширования
        :return: хэш
        """
        h = 0
        for i in range(length):
            h = (h + math.pow(ord(string[i]), 2)) % self._Q
        return h

    def _get_updated_hash(
        self, h: int, string: str, index_of_first_char: int, length: int
    ):
        """
        Возвращает хэш для строки, сдвинутой относительно предыдущей на один символ

        :param h: текущий хэш
        :param string: строка, для которой вычисляется хэш
        :param index_of_first_char: индекс первого символа, который использовался для подсчета хэша
        :param length: количество символов строки (начиная с 0), которые используются для хэширования
        :return: обновленный хэш
        """
        h = (h + math.pow(ord(string[index_of_first_char + length]), 2)) % self._Q
        return (
            h + self._Q - math.pow(ord(string[index_of_first_char]), 2) % self._Q
        ) % self._Q

    @staticmethod
    def _compare(string: str, substring: str, start_index: int) -> bool:
        """
        Сравнивает строку substring со строкой string, начиная с индекса start_index

        :param start_index: индекс для строки string, с которого начинается сравнение
        :return: строки совпали -> True, иначе -> False
        """
        for shift in range(len(substring)):
            if string[start_index + shift] != substring[shift]:
                return False
        return True
