from abstract_substring_searcher import AbstractSubstringSearcher


class BruteForce(AbstractSubstringSearcher):
    def search(self, string: str, substring: str) -> list[int]:
        if len(string) < len(substring):
            return []
        indexes = []
        for start_index in range(len(string) - len(substring) + 1):
            substring_found = True
            for shift in range(len(substring)):
                if string[start_index + shift] != substring[shift]:
                    substring_found = False
                    break
            if substring_found:
                indexes.append(start_index)
        return indexes