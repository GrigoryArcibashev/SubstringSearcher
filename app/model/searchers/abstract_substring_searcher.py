from abc import abstractmethod


class AbstractSubstringSearcher:
    """Абстрактный класс для алгоритма поиска подстроки в строке"""

    @abstractmethod
    def search(self, string: str, substring: str) -> list[int]:
        """
        Ищет все вхождения подстроки в строке

        :param string: строка
        :param substring: подстрока
        :return: список индексов в строке string, где начинается подстрока substring
        """
        pass
