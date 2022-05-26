import pytest

from app.model.searchers.abstract_substring_searcher import AbstractSubstringSearcher
from app.model.searchers.aho_korasik_searcher import AhoKorasikSearcher
from app.model.searchers.boyer_moore_searcher import BoyerMooreSearcher
from app.model.searchers.brute_force_searcher import BruteForceSearcher
from app.model.searchers.kmp_searcher import KMPSearcher
from app.model.searchers.rabin_karp_searcher.rabin_karp_polynomial_hash import (
    RabinKarpWithPolynomialHashSearcher,
)
from app.model.searchers.rabin_karp_searcher.rabin_karp_square_hash import (
    RabinKarpWithSquareHashSearcher,
)
from tests import (
    aho_korasik_searcher,
    boyer_moore_searcher,
    brute_force_searcher,
    check_search_indexes,
    kmp_searcher,
    rabin_karp_with_polynomial_hash_searcher,
    rabin_karp_with_square_hash_searcher,
)


class TestsCommonCases:
    @staticmethod
    def _check(
        string: str,
        substring: str,
        searcher: AbstractSubstringSearcher,
        expected: list[int],
    ):
        actual = searcher.search(string, substring)

        assert actual == expected

    @pytest.mark.parametrize(
        "string, substring, searcher, expected",
        [
            ("str", "sub", brute_force_searcher, []),
            ("str", "str", brute_force_searcher, [0]),
            ("str", "sub", rabin_karp_with_polynomial_hash_searcher, []),
            ("str", "str", rabin_karp_with_polynomial_hash_searcher, [0]),
            ("str", "sub", rabin_karp_with_square_hash_searcher, []),
            ("str", "str", rabin_karp_with_square_hash_searcher, [0]),
            ("str", "sub", aho_korasik_searcher, []),
            ("str", "str", aho_korasik_searcher, [0]),
            ("str", "sub", boyer_moore_searcher, []),
            ("str", "str", boyer_moore_searcher, [0]),
            ("str", "sub", kmp_searcher, []),
            ("str", "str", kmp_searcher, [0]),
        ],
    )
    def test__non_empty_string_and_substring_of_same_length(
        self,
        string: str,
        substring: str,
        searcher: AbstractSubstringSearcher,
        expected: list[int],
    ):
        check_search_indexes(string, substring, searcher, expected)

    @pytest.mark.parametrize(
        "string, substring, searcher",
        [
            ("Python", "th", brute_force_searcher),
            ("Python", "th", rabin_karp_with_polynomial_hash_searcher),
            ("Python", "th", rabin_karp_with_square_hash_searcher),
            ("Python", "th", aho_korasik_searcher),
            ("Python", "th", boyer_moore_searcher),
            ("Python", "th", kmp_searcher),
        ],
    )
    def test__one_coincidence(
        self,
        string: str,
        substring: str,
        searcher: AbstractSubstringSearcher,
    ):
        check_search_indexes(string, substring, searcher, [2])

    @pytest.mark.parametrize(
        "string, substring, searcher, expected",
        [
            ("aa", "a", brute_force_searcher, [0, 1]),
            ("aba", "a", brute_force_searcher, [0, 2]),
            ("aba aba", "aba", brute_force_searcher, [0, 4]),
            ("aba aba  aba", "aba", brute_force_searcher, [0, 4, 9]),
            ("aa", "a", rabin_karp_with_polynomial_hash_searcher, [0, 1]),
            ("aba", "a", rabin_karp_with_polynomial_hash_searcher, [0, 2]),
            ("aba aba", "aba", rabin_karp_with_polynomial_hash_searcher, [0, 4]),
            (
                "aba aba  aba",
                "aba",
                rabin_karp_with_polynomial_hash_searcher,
                [0, 4, 9],
            ),
            ("aa", "a", rabin_karp_with_square_hash_searcher, [0, 1]),
            ("aba", "a", rabin_karp_with_square_hash_searcher, [0, 2]),
            ("aba aba", "aba", rabin_karp_with_square_hash_searcher, [0, 4]),
            ("aba aba  aba", "aba", rabin_karp_with_square_hash_searcher, [0, 4, 9]),
            ("aa", "a", aho_korasik_searcher, [0, 1]),
            ("aba", "a", aho_korasik_searcher, [0, 2]),
            ("aba aba", "aba", aho_korasik_searcher, [0, 4]),
            ("aba aba  aba", "aba", aho_korasik_searcher, [0, 4, 9]),
            ("aa", "a", boyer_moore_searcher, [0, 1]),
            ("aba", "a", boyer_moore_searcher, [0, 2]),
            ("aba aba", "aba", boyer_moore_searcher, [0, 4]),
            ("aba aba  aba", "aba", boyer_moore_searcher, [0, 4, 9]),
            ("aa", "a", kmp_searcher, [0, 1]),
            ("aba", "a", kmp_searcher, [0, 2]),
            ("aba aba", "aba", kmp_searcher, [0, 4]),
            ("aba aba  aba", "aba", kmp_searcher, [0, 4, 9]),
        ],
    )
    def test__several_coincidences(
        self,
        string: str,
        substring: str,
        searcher: AbstractSubstringSearcher,
        expected: list[int],
    ):
        check_search_indexes(string, substring, searcher, expected)

    @pytest.mark.parametrize(
        "string, substring, searcher",
        [
            ("fsfsf", "fsf", brute_force_searcher),
            ("fsfsf", "fsf", rabin_karp_with_polynomial_hash_searcher),
            ("fsfsf", "fsf", rabin_karp_with_square_hash_searcher),
            ("fsfsf", "fsf", aho_korasik_searcher),
            ("fsfsf", "fsf", boyer_moore_searcher),
            ("fsfsf", "fsf", kmp_searcher),
        ],
    )
    def test__overlapping_coincidences(
        self,
        string: str,
        substring: str,
        searcher: AbstractSubstringSearcher,
    ):
        check_search_indexes(string, substring, searcher, [0, 2])
