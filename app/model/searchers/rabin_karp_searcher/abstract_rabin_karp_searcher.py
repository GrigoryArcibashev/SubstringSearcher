from abc import abstractmethod

from app.model.searchers.abstract_substring_searcher import AbstractSubstringSearcher


class AbstractRabinKarpSearcher(AbstractSubstringSearcher):
    """Абстрактный класс для алгоритма Рабина-Карпа"""

    def search(self, string: str, substring: str) -> list[int]:
        indexes = []
        str_hash = self._get_hash(string, len(substring))
        substr_hash = self._get_hash(substring, len(substring))
        for i in range(len(string) - len(substring)):
            if str_hash == substr_hash:
                if self._compare(string, substring, i):
                    indexes.append(i)
            str_hash = self._get_updated_hash(str_hash, string, i, len(substring))
        return indexes

    @abstractmethod
    def _get_hash(self, string: str, length: int) -> int:
        """
        Возвращает хэш для строки

        :param string: строка, для которой вычисляется хэш
        :param length: количество символов строки (начиная с 0), которые используются для хэширования
        :return: хэш
        """
        pass

    @abstractmethod
    def _get_updated_hash(
        self, hash: int, string: str, index_of_first_char: int, length: int
    ) -> int:
        """
        Возвращает хэш для строки, сдвинутой относительно предыдущей на один символ

        :param hash: текущий хэш
        :param string: строка, для которой вычисляется хэш
        :param index_of_first_char: индекс первого символа, который использовался для подсчета хэша
        :param length: количество символов строки (начиная с 0), которые используются для хэширования
        :return: обновленный хэш
        """
        pass

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
