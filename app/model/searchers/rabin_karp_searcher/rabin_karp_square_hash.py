import math

from app.model.searchers.rabin_karp_searcher.abstract_rabin_karp_searcher import (
    AbstractRabinKarpSearcher,
)


class RabinKarpWithSquareHashSearcher(AbstractRabinKarpSearcher):
    """Класс для алгоритма Рабина-Карпа с хэшем на сумме квадратов"""

    def _get_hash(self, string: str, length: int) -> int:
        hash = 0
        for i in range(length):
            hash += math.pow(ord(string[i]), 2)
        return hash

    def _get_updated_hash(
        self, hash: int, string: str, index_of_first_char: int, length: int
    ):
        hash += math.pow(ord(string[index_of_first_char + length]), 2)
        return hash - math.pow(ord(string[index_of_first_char]), 2)
