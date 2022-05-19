from abc import abstractmethod


class AbstractSubstringSearcher:
    @abstractmethod
    def search(self, string: str, substring: str) -> list[int]:
        pass
