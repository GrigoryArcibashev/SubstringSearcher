import math
from abc import abstractmethod

from abstract_substring_searcher import AbstractSubstringSearcher


class AbstractRabinKarpSearcher(AbstractSubstringSearcher):
    def search(self, string: str, substring: str) -> list[int]:
        indexes = []
        str_hash = self._get_hash(
                string,
                len(substring))
        substr_hash = self._get_hash(
                substring,
                len(substring))
        for i in range(len(string) - len(substring)):
            if str_hash == substr_hash:
                if self._compare(string, substring, i):
                    indexes.append(i)
            str_hash = self._get_updated_hash(
                    str_hash,
                    string,
                    i,
                    len(substring))
        return indexes

    @abstractmethod
    def _get_hash(self, string: str, max_power: int) -> int:
        pass

    @abstractmethod
    def _get_updated_hash(
            self,
            hash: int,
            string: str,
            index_of_first_char: int,
            max_power: int) -> int:
        pass

    def _compare(self, string: str, substring: str, start_index: int) -> bool:
        for shift in range(len(substring)):
            if string[start_index + shift] != substring[shift]:
                return False
        return True


class RabinKarpWithPolynomialHashSearcher(AbstractRabinKarpSearcher):

    def _get_hash(self, string: str, max_power: int) -> int:
        hash = 0
        for i in range(max_power):
            hash += ord(string[i]) * math.pow(2, max_power - i - 1)
        return hash

    def _get_updated_hash(
            self,
            hash: int,
            string: str,
            index_of_first_char: int,
            max_power: int):
        hash -= ord(string[index_of_first_char]) * math.pow(2, max_power - 1)
        return hash * 2 + ord(string[index_of_first_char + max_power])


class RabinKarpWithSquareHashSearcher(AbstractRabinKarpSearcher):
    def _get_hash(self, string: str, max_power: int) -> int:
        hash = 0
        for i in range(max_power):
            hash += math.pow(ord(string[i]), 2)
        return hash

    def _get_updated_hash(
            self,
            hash: int,
            string: str,
            index_of_first_char: int,
            max_power: int):
        hash += math.pow(ord(string[index_of_first_char + max_power]), 2)
        return hash - math.pow(ord(string[index_of_first_char]), 2)
