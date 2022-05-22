from typing import Optional

from app.model.searchers.abstract_substring_searcher import AbstractSubstringSearcher


class AhoKorasikSearcher(AbstractSubstringSearcher):
    """Класс для алгоритма Ахо-Корасика"""

    def search(self, string: str, substring: str) -> list[int]:
        indexes = []
        bohr = Bohr()
        bohr.add(substring)
        vertex = bohr.root
        for i in range(len(string)):
            vertex = bohr.go(vertex, string[i])
            if vertex.is_terminal:
                indexes.append(i - len(substring) + 1)
        return indexes


class Vertex:
    """Класс вершины бора"""

    def __init__(self, parent: Optional, parent_char: Optional[str]):
        """
        :param parent: родитель вершины (так же Vertex)
        :param parent_char: символ, по которому осуществляется переход из родительской вершины в данную
        """
        self.parent: Optional = parent
        self.parent_char: Optional[str] = parent_char
        self.next: dict[int, Vertex] = dict()
        self.go: dict[int, Vertex] = dict()
        self.suffix_link = None
        self.is_terminal: bool = False


class Bohr:
    """Класс бора"""

    def __init__(self):
        self._vertices: list[Vertex] = [Vertex(None, None)]
        self.root: Vertex = self._vertices[0]

    @property
    def _last(self) -> Vertex:
        """
        :return: последняя добавленная вершина
        """
        return self._vertices[-1]

    def add(self, string: str) -> None:
        """
        Добавляет строку в бор

        :param string: добавляемая строка
        :return: None
        """
        vertex = self.root
        for i in range(len(string)):
            if vertex.next.get(ord(string[i]), None) is None:
                self._vertices.append(Vertex(vertex, string[i]))
                vertex.next[ord(string[i])] = self._last
            vertex = vertex.next[ord(string[i])]

        vertex.is_terminal = True

    def _get_link(self, vertex: Vertex) -> Vertex:
        """
        Возвращает (при необходимости вычисляет) суффиксную ссылку для вершины

        :param vertex: вершина, для которой нужно вернуть суффиксную ссылку
        :return: вершина, на которую указывает суффиксная ссылка
        """
        if vertex.suffix_link is None:
            if vertex == self.root or vertex.parent == self.root:
                vertex.suffix_link = self.root
            else:
                vertex.suffix_link = self.go(
                    self._get_link(vertex.parent), vertex.parent_char
                )
        return vertex.suffix_link

    def go(self, vertex: Vertex, char: str) -> Vertex:
        """
        Функция перехода из одной вершины в боре в другую

        :param vertex: исходная вершина, из которой осуществляется переход
        :param char: символ, по которому осуществляется переход
        :return: вершина, в которую был осуществлен переход
        """
        if vertex.go.get(ord(char), None) is None:
            if vertex.next.get(ord(char), None) is not None:
                vertex.go[ord(char)] = vertex.next[ord(char)]
            elif vertex == self.root:
                vertex.go[ord(char)] = self.root
            else:
                vertex.go[ord(char)] = self.go(self._get_link(vertex), char)
        return vertex.go[ord(char)]
