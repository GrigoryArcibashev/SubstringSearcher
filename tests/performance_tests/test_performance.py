from app.model.searchers.abstract_substring_searcher import AbstractSubstringSearcher
from app.model.utils.stopwatch import Stopwatch
from tests import (
    aho_korasik_searcher,
    boyer_moore_searcher,
    brute_force_searcher,
    kmp_searcher,
    rabin_karp_with_polynomial_hash_searcher,
    rabin_karp_with_square_hash_searcher,
)
from tests.performance_tests import long_string_of_one_char


class Tests:
    @staticmethod
    def _get_work_time_of_searching(
        string: str, substring: str, searcher: AbstractSubstringSearcher
    ) -> float:
        stopwatch = Stopwatch()
        stopwatch.start()
        searcher.search(string, substring)
        stopwatch.stop()
        return stopwatch.get_time_in_seconds()

    def test__long_string_of_one_char(self):
        substring = "a" * 3000
        bf_time = self._get_work_time_of_searching(
            long_string_of_one_char, substring, brute_force_searcher
        )
        rk_sq_time = self._get_work_time_of_searching(
            long_string_of_one_char, substring, rabin_karp_with_square_hash_searcher
        )
        rk_pol_time = self._get_work_time_of_searching(
            long_string_of_one_char, substring, rabin_karp_with_polynomial_hash_searcher
        )
        bm_time = self._get_work_time_of_searching(
            long_string_of_one_char, substring, boyer_moore_searcher
        )
        kmp_time = self._get_work_time_of_searching(
            long_string_of_one_char, substring, kmp_searcher
        )
        print(f"\n\nBF: {bf_time}\nSq: {rk_sq_time}\nPol: {rk_pol_time}")
        print(f"BM: {bm_time}\nKMP: {kmp_time}\n")
        assert rk_pol_time < bf_time
        assert kmp_time < rk_sq_time
        assert kmp_time < rk_pol_time
        assert kmp_time < bm_time
        assert kmp_time < bf_time

    def test__GTA1024(self):
        pass

    def test__long_string_of_one_char_but_other_char_in_begin(self):
        pass

    def test__long_string_of_one_char_but_other_char_in_end(self):
        pass

    def test__war_and_peace(self):
        pass
