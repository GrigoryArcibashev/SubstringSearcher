from collections import deque
from enum import Enum
from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QTextDocument


class BlockState(Enum):
    """Вспомогательный класс для алгоритма поиска вхождений строки в тексте"""

    PREV_BLOCK_IS_PROCESSED = 0
    PREV_BLOCK_IS_NOT_PROCESSED = 1


class HighLighter(QSyntaxHighlighter):
    """Класс, отвечающий за подсветку найденных вхождений строки в тексте"""

    def __init__(self, parent: QTextDocument):
        super().__init__(parent)
        self._reset()
        self._format = QTextCharFormat()
        self._format.setBackground(Qt.green)

    @staticmethod
    def _get_indexes_of_gaps_for_highlighting(
            search_result: list[int],
            substring_length: int) -> list[tuple[int, int]]:
        """
        Возвращает индексы интервалов для подсветки найденных шаблонов в тексте
        """
        return list(
            map(lambda index: (index, substring_length), search_result)
        )

    def highlightBlock(self, text) -> None:
        block_len = len(text)
        while (
                len(self._indexes) > 0
                or self._state == BlockState.PREV_BLOCK_IS_NOT_PROCESSED
        ):
            if self._state == BlockState.PREV_BLOCK_IS_PROCESSED:
                self._current_index = self._indexes.popleft()
            start = self._current_index[0] - self._cursor
            count = self._current_index[1]
            if block_len <= start:
                self._cursor += block_len + 1
                self._state = BlockState.PREV_BLOCK_IS_NOT_PROCESSED
                return
            start = max(0, start)
            if block_len - start < count - self._count_of_highlighted_symbols:
                self.setFormat(start, block_len - start, self._format)
                self._count_of_highlighted_symbols += block_len - start + 1
                self._cursor += block_len + 1
                self._state = BlockState.PREV_BLOCK_IS_NOT_PROCESSED
                return
            self.setFormat(
                start, count - self._count_of_highlighted_symbols,
                self._format
            )
            self._count_of_highlighted_symbols = 0
            self._state = BlockState.PREV_BLOCK_IS_PROCESSED

    def highlight_found_occurrences(
            self,
            search_result: list[int],
            substring_length: int) -> None:
        """
        Подсвечивает найденные вхождения строки в тексте

        :param search_result: индексы вхождений [start_index, ...]
        :param substring_length: длина шаблона
        """

        self._reset()
        for ind in self._get_indexes_of_gaps_for_highlighting(
                search_result, substring_length):
            self._indexes.append(ind)
        self.rehighlight()

    def _reset(self) -> None:
        """Сбрасывает все настройки"""
        self._state = BlockState.PREV_BLOCK_IS_PROCESSED
        self._indexes: deque[tuple[int, int]] = deque()
        self._current_index: Optional[tuple[int, int]] = None
        self._cursor: int = 0
        self._count_of_highlighted_symbols: int = 0
