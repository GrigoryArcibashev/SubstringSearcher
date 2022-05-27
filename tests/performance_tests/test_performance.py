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
from tests.performance_tests import (
    long_string_of_one_char,
    long_string_of_one_char_but_other_char_in_begin,
    long_string_of_one_char_but_other_char_in_end,
    TGCA,
    war_and_peace,
)


class Tests:
    @staticmethod
    def _get_work_time_of_searching_in_seconds(
        string: str, substring: str, searcher: AbstractSubstringSearcher
    ) -> float:
        """
        Замеряет время работы алгоритма

        :param string: строка
        :param substring: подстрока
        :param searcher: алгоритм поиска
        :return: время работы алгоритма в секундах
        """
        stopwatch = Stopwatch()
        stopwatch.start()
        searcher.search(string, substring)
        stopwatch.stop()
        return stopwatch.get_time_in_seconds()

    def test__when_brute_force_has_same_performance_as_rabin_karp(self) -> None:
        """
        Строка состоит из большого количества подряд идущих букв 'a',
        искомая подстрока состоит из подряд идущих букв 'a'

        :return: None
        """
        substring = "a" * 3000
        bf_time, rk_pol_time, rk_sq_time = self._get_work_time_of_bf_and_rk(
            long_string_of_one_char, substring, 5
        )
        print(f"\n\nBF: {bf_time}\nSq: {rk_sq_time}\nPol: {rk_pol_time}")
        assert abs(rk_pol_time - bf_time) < 0.2
        assert abs(rk_sq_time - bf_time) < 0.2

    def test__when_brute_force_is_faster_than_rabin_karp(self) -> None:
        """
        Строка состоит из большого количества подряд идущих букв 'a',
        искомая подстрока состоит из подряд идущих букв 'a',
        в начале подстроки стоит буква 'b'

        :return: None
        """
        substring = "b" + "a" * 2000
        bf_time, rk_pol_time, rk_sq_time = self._get_work_time_of_bf_and_rk(
            long_string_of_one_char, substring, 5
        )
        print(f"\n\nBF: {bf_time}\nSq: {rk_sq_time}\nPol: {rk_pol_time}")
        assert bf_time < rk_sq_time
        assert bf_time < rk_pol_time

    def test__when_brute_force_is_slower_than_rabin_karp(self) -> None:
        """
        Строка состоит из большого количества подряд идущих букв 'a',
        искомая подстрока состоит из подряд идущих букв 'a',
        в конце подстроки стоит буква 'b'

        :return: None
        """
        substring = "a" * 2000 + "b"
        bf_time, rk_pol_time, rk_sq_time = self._get_work_time_of_bf_and_rk(
            long_string_of_one_char, substring, 5
        )
        print(f"\n\nBF: {bf_time}\nSq: {rk_sq_time}\nPol: {rk_pol_time}")
        assert rk_sq_time < bf_time
        assert rk_pol_time < bf_time

    def _get_work_time_of_bf_and_rk(
        self, string: str, substring: str, count_of_measurements: int
    ) -> tuple[float, float, float]:
        """
        Возвращает среднее время работы алгоритмов BruteForce, RabinKarp (square hash) и RabinKarp (polynomial hash)

        :param string: строка
        :param substring: подстрока
        :param count_of_measurements: количество замеров производительности
        :return: среднее время работы алгоритмов поиска по порядку: BruteForce, RabinKarp (square hash), RabinKarp (polynomial hash)
        """
        bf_time = rk_sq_time = rk_pol_time = 0
        for _ in range(count_of_measurements):
            bf_time += self._get_work_time_of_searching_in_seconds(
                string, substring, brute_force_searcher
            )
            rk_sq_time += self._get_work_time_of_searching_in_seconds(
                string, substring, rabin_karp_with_square_hash_searcher
            )
            rk_pol_time += self._get_work_time_of_searching_in_seconds(
                string,
                substring,
                rabin_karp_with_polynomial_hash_searcher,
            )
        return (
            bf_time / count_of_measurements,
            rk_pol_time / count_of_measurements,
            rk_sq_time / count_of_measurements,
        )
