import math

from app.model.searchers.rabin_karp_searcher.abstract_rabin_karp_searcher import \
    AbstractRabinKarpSearcher


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
