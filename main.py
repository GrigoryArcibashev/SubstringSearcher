from app.searchers.aho_korasik_searcher import AhoKorasikSearcher
from app.searchers.boyer_moore_searcher import BoyerMooreSearcher
from app.searchers.brute_force_searcher import BruteForce
from app.searchers.kmp_searcher import KMPSearcher
from app.searchers.rabin_karp_searcher.rabin_karp_polynomial_hash import \
    RabinKarpWithPolynomialHashSearcher
from app.searchers.rabin_karp_searcher.rabin_karp_square_hash import \
    RabinKarpWithSquareHashSearcher


def main():
    KMPSearcher().search('abbAba', 'ba')
    RabinKarpWithPolynomialHashSearcher().search('abbAba', 'ba')
    RabinKarpWithSquareHashSearcher().search('abbAba', 'ba')
    BruteForce().search('abbAba', 'ba')
    BoyerMooreSearcher().search('abbAba', 'ba')
    AhoKorasikSearcher().search('abbAba', 'ba')


if __name__ == "__main__":
    main()
