from app.model.searchers.abstract_substring_searcher import \
    AbstractSubstringSearcher
from app.model.searchers.aho_korasik_searcher import AhoKorasikSearcher
from app.model.searchers.boyer_moore_searcher import BoyerMooreSearcher
from app.model.searchers.brute_force_searcher import BruteForceSearcher
from app.model.searchers.kmp_searcher import KMPSearcher
from app.model.searchers.rabin_karp_searcher.polynomial_hash import \
    RabinKarpWithPolynomialHashSearcher
from app.model.searchers.rabin_karp_searcher.square_hash import \
    RabinKarpWithSquareHashSearcher

brute_force_searcher = BruteForceSearcher()
rabin_karp_with_pol_hash_searcher = RabinKarpWithPolynomialHashSearcher()
rabin_karp_with_square_hash_searcher = RabinKarpWithSquareHashSearcher()
aho_korasik_searcher = AhoKorasikSearcher()
boyer_moore_searcher = BoyerMooreSearcher()
kmp_searcher = KMPSearcher()


def check_search_indexes(
    string: str,
    substring: str,
    searcher: AbstractSubstringSearcher,
    expected: list[int],
) -> None:
    """
    Проверяет результат поиска подстроки в строки searcher-ом с expected

    :param string: строка
    :param substring: подстрока
    :param searcher: алгоритм поиска
    :param expected: список ожидаемых индексов
    :return: None, используется assert
    """
    actual = searcher.search(string, substring)

    assert actual == expected
