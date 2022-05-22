import math

from app.model.searchers.rabin_karp_searcher.abstract_rabin_karp_searcher import (
    AbstractRabinKarpSearcher,
)


class RabinKarpWithPolynomialHashSearcher(AbstractRabinKarpSearcher):
    """Класс для алгоритма Рабина-Карпа с полиномиальным хэшем"""

    def _get_hash(self, string: str, length: int) -> int:
        hash = 0
        for i in range(length):
            hash += ord(string[i]) * math.pow(2, length - i - 1)
        return hash

    def _get_updated_hash(
        self, hash: int, string: str, index_of_first_char: int, length: int
    ):
        hash -= ord(string[index_of_first_char]) * math.pow(2, length - 1)
        return hash * 2 + ord(string[index_of_first_char + length])
