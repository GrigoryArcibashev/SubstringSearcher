import pytest

from app.model.searchers.abstract_substring_searcher import AbstractSubstringSearcher
from tests import (
    aho_korasik_searcher,
    boyer_moore_searcher,
    brute_force_searcher,
    kmp_searcher,
    rabin_karp_with_polynomial_hash_searcher,
    rabin_karp_with_square_hash_searcher,
)


class TestsBoundaryCases:
    @pytest.mark.parametrize(
        "searcher",
        [
            brute_force_searcher,
            rabin_karp_with_polynomial_hash_searcher,
            rabin_karp_with_square_hash_searcher,
            aho_korasik_searcher,
            boyer_moore_searcher,
            kmp_searcher,
        ],
    )
    def test__empty_string_and_substring(self, searcher: AbstractSubstringSearcher):
        actual = searcher.search("", "")

        assert actual == []

    @pytest.mark.parametrize(
        "searcher",
        [
            brute_force_searcher,
            rabin_karp_with_polynomial_hash_searcher,
            rabin_karp_with_square_hash_searcher,
            aho_korasik_searcher,
            boyer_moore_searcher,
            kmp_searcher,
        ],
    )
    def test__empty_string_and_non_empty_substring(
        self, searcher: AbstractSubstringSearcher
    ):
        actual = searcher.search("", "substring")

        assert actual == []

    @pytest.mark.parametrize(
        "searcher",
        [
            brute_force_searcher,
            rabin_karp_with_polynomial_hash_searcher,
            rabin_karp_with_square_hash_searcher,
            aho_korasik_searcher,
            boyer_moore_searcher,
            kmp_searcher,
        ],
    )
    def test__non_empty_string_and_empty_substring(
        self, searcher: AbstractSubstringSearcher
    ):
        actual = searcher.search("string", "")

        assert actual == []

    @pytest.mark.parametrize(
        "string, substring, searcher",
        [
            ("str", "string", brute_force_searcher),
            ("ing", "string", brute_force_searcher),
            ("str", "string", rabin_karp_with_polynomial_hash_searcher),
            ("ing", "string", rabin_karp_with_polynomial_hash_searcher),
            ("str", "string", rabin_karp_with_square_hash_searcher),
            ("ing", "string", rabin_karp_with_square_hash_searcher),
            ("str", "string", aho_korasik_searcher),
            ("ing", "string", aho_korasik_searcher),
            ("str", "string", boyer_moore_searcher),
            ("ing", "string", boyer_moore_searcher),
            ("str", "string", kmp_searcher),
            ("ing", "string", kmp_searcher),
        ],
    )
    def test__length_of_string_less_than_length_of_substring(
        self,
        string: str,
        substring: str,
        searcher: AbstractSubstringSearcher,
    ):
        actual = searcher.search(string, substring)

        assert actual == []
