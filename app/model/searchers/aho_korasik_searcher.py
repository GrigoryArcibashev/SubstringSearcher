from typing import Optional

from memory_profiler import profile

from app.model.searchers.abstract_substring_searcher import AbstractSubstringSearcher
from app.model.utils.stopwatch_decorator import stopwatch


def num(char: str) -> int:
    return ord(char) - ord('a')


class AhoKorasikSearcher(AbstractSubstringSearcher):
    @stopwatch()
    @profile
    def search(self, string: str, substring: str) -> list[int]:
        indexes = []
        trie = Trie()
        trie.add(substring)
        vertex = trie.root
        for i in range(len(string)):
            vertex = trie.go(vertex, string[i])
            if vertex.is_terminal:
                indexes.append(i - len(substring) + 1)
        return indexes


class Vertex:
    def __init__(self, parent: Optional, parent_char: Optional[str]):
        self.parent: Optional = parent
        self.parent_char: Optional[str] = parent_char
        self.next: dict[int, Vertex] = dict()
        self.go: dict[int, Vertex] = dict()
        self.suffix_link = None
        self.is_terminal: bool = False


class Trie:
    def __init__(self):
        self._vertices: list[Vertex] = [Vertex(None, None)]
        self.root: Vertex = self._vertices[0]

    @property
    def size(self) -> int:
        return len(self._vertices)

    @property
    def last(self) -> Vertex:
        return self._vertices[-1]

    def add(self, string: str) -> None:
        vertex = self.root
        for i in range(len(string)):
            if vertex.next.get(num(string[i]), None) is None:
                self._vertices.append(
                        Vertex(
                                vertex,
                                string[i]
                        )
                )
                vertex.next[num(string[i])] = self.last
            vertex = vertex.next[num(string[i])]

        vertex.is_terminal = True

    def get_link(self, vertex: Vertex) -> Vertex:
        if vertex.suffix_link is None:
            if vertex == self.root or vertex.parent == self.root:
                vertex.suffix_link = self.root
            else:
                vertex.suffix_link = self.go(
                        self.get_link(vertex.parent),
                        vertex.parent_char)
        return vertex.suffix_link

    def go(self, vertex: Vertex, char: str) -> Vertex:
        if vertex.go.get(num(char), None) is None:
            if vertex.next.get(num(char), None) is not None:
                vertex.go[num(char)] = vertex.next[num(char)]
            elif vertex == self.root:
                vertex.go[num(char)] = self.root
            else:
                vertex.go[num(char)] = self.go(self.get_link(vertex), char)
        return vertex.go[num(char)]
