from app.model.searchers.abstract_substring_searcher import \
    AbstractSubstringSearcher
from app.model.utils.stopwatch import Stopwatch
from tests import (
    aho_korasik_searcher, boyer_moore_searcher,
    brute_force_searcher, kmp_searcher,
    rabin_karp_with_polynomial_hash_searcher,
    rabin_karp_with_square_hash_searcher)
from tests.performance_tests import long_string_of_one_char, war_and_peace


class Tests:
    def test__common_test(self):
        """
        Строка - большой кусок "Войны и мира" (~78000 символов),
        подстрока - "князь Андрей Болконский"

        ----

        Бойер-Мур быстрее всех, полиномиальные хеши - медленнее всех;

        КМП быстрее грубой силы, Ахо-Корасика и квадратичных хешей;

        Грубая сила, Ахо-Корасик и квадратичные хеши по времени работы
        отличаются друг от друга не более, чем на 0.3 секунды
        """
        (
            bf_time,
            rk_pol_time,
            rk_sq_time,
            aho_time,
            bm_time,
            kmp_time
            ) = self._get_work_time_of_searchers(
                war_and_peace,
                "князь Андрей Болконский",
                5,
                [
                    brute_force_searcher,
                    rabin_karp_with_square_hash_searcher,
                    rabin_karp_with_polynomial_hash_searcher,
                    aho_korasik_searcher,
                    boyer_moore_searcher,
                    kmp_searcher
                    ]
                )
        all_times = (
            aho_time, bf_time, bm_time, kmp_time, rk_pol_time, rk_sq_time
            )
        for time in all_times:
            assert bm_time <= time <= rk_pol_time
        for time in (bf_time, rk_sq_time, aho_time):
            assert kmp_time <= time
        assert abs(bf_time - aho_time) < 0.3
        assert abs(bf_time - rk_sq_time) < 0.3
        assert abs(rk_sq_time - aho_time) < 0.3

    # TESTS FOR A VERY LONG TIME
    def test__when_brute_force_has_same_performance_as_rabin_karp(
            self
            ) -> None:
        """
        Строка - 16000 подряд идущих букв 'a',
        подстрока - 3000 подряд идущих букв 'a'

        ----

        Грубая сила работает примерно за то же время,
        что и Рабин-Карп (квадр. и полин. хеши)
        """
        substring = "a" * 3000
        bf_time, rk_pol_time, rk_sq_time = self._get_work_time_of_bf_and_rk(
                long_string_of_one_char,
                substring,
                5
                )
        print(f"\n\nBF: {bf_time}\nSq: {rk_sq_time}\nPol: {rk_pol_time}")
        assert abs(rk_pol_time - bf_time) < 2
        assert abs(rk_sq_time - bf_time) < 2

    def test__when_brute_force_is_faster_than_rabin_karp(self) -> None:
        """
        Строка - 16000 подряд идущих букв 'a',
        подстрока - буква 'b', после которой идут 2000 букв 'a'

        ----

        Грубая сила быстрее Рабина-Карпа (квадр. и полин. хеши)
        """
        substring = "b" + "a" * 2000
        bf_time, rk_pol_time, rk_sq_time = self._get_work_time_of_bf_and_rk(
                long_string_of_one_char,
                substring,
                5
                )
        print(f"\n\nBF: {bf_time}\nSq: {rk_sq_time}\nPol: {rk_pol_time}")
        assert bf_time < rk_sq_time
        assert bf_time < rk_pol_time

    # TESTS FOR A VERY LONG TIME
    def test__when_brute_force_is_slower_than_rabin_karp(self) -> None:
        """
        Строка - 16000 подряд идущих букв 'a',
        подстрока - 2000 подряд идущих букв 'a', после которых идет буква 'b'

        ----

        Грубая сила медленнее Рабина-Карпа (квадр. и полин. хеши)
        """
        substring = "a" * 2000 + "b"
        bf_time, rk_pol_time, rk_sq_time = self._get_work_time_of_bf_and_rk(
                long_string_of_one_char,
                substring,
                5
                )
        print(f"\n\nBF: {bf_time}\nSq: {rk_sq_time}\nPol: {rk_pol_time}")
        assert rk_sq_time < bf_time
        assert rk_pol_time < bf_time

    @staticmethod
    def _get_work_time_of_searching_in_seconds(
            string: str,
            substring: str,
            searcher: AbstractSubstringSearcher
            ) -> float:
        """Замеряет время работы алгоритма в секундах"""
        stopwatch = Stopwatch()
        stopwatch.start()
        searcher.search(string, substring)
        stopwatch.stop()
        return stopwatch.get_time_in_seconds()

    def _get_work_time_of_bf_and_rk(
            self,
            string,
            substring: str,
            count_of_measurements: int
            ) -> list[float, float, float]:
        """
        Возвращает среднее время работы алгоритмов BruteForce,
        RabinKarp (square hash) и RabinKarp (polynomial hash)

        :param count_of_measurements: количество замеров производительности
        :return: среднее время работы алгоритмов поиска по порядку:
        BruteForce, RabinKarp (square hash), RabinKarp (polynomial hash)
        """
        return self._get_work_time_of_searchers(
                string,
                substring,
                count_of_measurements,
                [
                    brute_force_searcher,
                    rabin_karp_with_square_hash_searcher,
                    rabin_karp_with_polynomial_hash_searcher,
                    ]
                )

    def _get_work_time_of_searchers(
            self,
            string: str,
            substring: str,
            count_of_measurements: int,
            searchers: list[AbstractSubstringSearcher]
            ) -> list[float]:
        """
        Возвращает среднее время работы указанных алгоритмов

        :param count_of_measurements: количество замеров производительности
        :param searchers: список серчеров (алгоритмов поиска)
        :return: среднее время работы алгоритмов поиска
        в порядке их указания в searchers
        """
        results = [0] * len(searchers)
        for _ in range(count_of_measurements):
            for i in range(len(searchers)):
                results[i] += self._get_work_time_of_searching_in_seconds(
                        string,
                        substring,
                        searchers[i]
                        )
        return results
