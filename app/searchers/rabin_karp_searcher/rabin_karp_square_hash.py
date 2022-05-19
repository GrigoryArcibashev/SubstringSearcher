import math

from app.searchers.rabin_karp_searcher.abstract_rabin_karp_searcher import \
    AbstractRabinKarpSearcher


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
