from app.searchers.aho_korasik_searcher import AhoKorasikSearcher
from app.searchers.boyer_moore_searcher import BoyerMooreSearcher
from app.searchers.brute_force_searcher import BruteForce
from app.searchers.kmp_searcher import KMPSearcher
from app.searchers.rabin_karp_searcher.rabin_karp_polynomial_hash import \
    RabinKarpWithPolynomialHashSearcher
from app.searchers.rabin_karp_searcher.rabin_karp_square_hash import \
    RabinKarpWithSquareHashSearcher
from app.searchers.z_asearcher import ZSearcher
from tests.reader import read_file


class Tests:
    _string = read_file('in.txt')

    def test__oak(self):
        sub_string = 'дуб'
        self._run_searchers(sub_string)

    def test__Andrey(self):
        sub_string = 'Андрей'
        self._run_searchers(sub_string)

    def test__oblomann(self):
        sub_string = 'обломанн'
        self._run_searchers(sub_string)

    def _run_searchers(self, sub_string):
        KMPSearcher().search(self._string, sub_string)
        RabinKarpWithPolynomialHashSearcher().search(self._string, sub_string)
        RabinKarpWithSquareHashSearcher().search(self._string, sub_string)
        BruteForce().search(self._string, sub_string)
        BoyerMooreSearcher().search(self._string, sub_string)
        AhoKorasikSearcher().search(self._string, sub_string)
        ZSearcher().search(self._string, sub_string)
