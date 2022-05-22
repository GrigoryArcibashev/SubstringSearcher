from collections import deque
from enum import Enum
from typing import Optional

from PyQt5.QtCore import QRect, QSize, Qt, pyqtSlot
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QTextDocument
from PyQt5.QtWidgets import (
    QComboBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QTextEdit,
)

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
from app.model.utils.file_reader import read_file


class Window(QMainWindow):
    """Класс главного окна GUI"""

    def __init__(self):
        super().__init__()
        self._init_searchers_by_name()
        self._init_window()
        self._init_menu_bar()
        self._init_text_viewer()
        self._init_labels()
        self._init_combo_of_searchers()
        self._init_substring_input()
        self._init_find_button()
        self._init_high_lighter()

    def _init_high_lighter(self) -> None:
        """Инициализирует подсветчика текста"""
        self._high_lighter = HighLighter(self._text_viewer.document())

    def _init_searchers_by_name(self) -> None:
        """Инициализирует словарь поисковиков по имени"""
        searchers = dict()
        searchers["Brute Force"] = BruteForceSearcher()
        searchers["Knut Morris Pratt"] = KMPSearcher()
        searchers[
            "Rabin Karp (Polynomial Hash)"
        ] = RabinKarpWithPolynomialHashSearcher()
        searchers["Rabin Karp (Square Hash)"] = RabinKarpWithSquareHashSearcher()
        searchers["Boyer Moore"] = BoyerMooreSearcher()
        searchers["Aho Korasik"] = AhoKorasikSearcher()
        self._searchers_by_name: dict[str, AbstractSubstringSearcher] = searchers

    def _init_window(self) -> None:
        """Инициализирует главное окно"""
        self.setWindowTitle("Substring searcher")
        self._size = QSize(800, 600)
        self.setGeometry(200, 200, self._size.width(), self._size.height())
        self.setFixedSize(self._size)

    def _init_text_viewer(self) -> None:
        """Инициализирует виджет для просмотра содержимого файла"""
        text_viewer = QTextEdit(self)
        text_viewer.setFont(QFont("Arial", 12))
        text_viewer.setReadOnly(True)
        size = QRect(10, 30, self._size.width() - 20, self._size.height() // 1.5)
        text_viewer.setGeometry(size)
        self._text_viewer = text_viewer

    def _init_menu_bar(self) -> None:
        """Инициализирует меню бар"""
        menu_bar = QMenuBar(self)
        menu_bar.setFont(QFont("Arial", 12))
        self.setMenuBar(menu_bar)
        file_menu = QMenu("&File", self)
        file_menu.setFont(QFont("Arial", 12))
        file_menu.addAction("&Open", self._action_open_file)
        menu_bar.addMenu(file_menu)

    def _init_combo_of_searchers(self) -> None:
        """Инициализирует интерфейс выбора алгоритма поиска"""
        searchers = QComboBox(self)
        size = QRect(150, self._size.height() // 1.5 + 50, 235, 30)
        searchers.setGeometry(size)
        searchers.setFont(QFont("Arial", 12))
        for name_of_searcher in self._searchers_by_name.keys():
            searchers.addItem(name_of_searcher)
        self._combo_of_searchers: QComboBox = searchers

    def _init_substring_input(self) -> None:
        """Инициализирует окно для ввода искомой строки"""
        sub_inp = QLineEdit(self)
        sub_inp.setFont(QFont("Arial", 12))
        size = QRect(150, self._size.height() // 1.5 + 90, 235, 30)
        sub_inp.setGeometry(size)
        self._substring_input = sub_inp

    def _init_labels(self) -> None:
        """Инициализирует все метки"""
        self._init_memory_label()
        self._init_time_label()
        self._init_selected_searcher_label()
        self._init_substring_label()

    def _init_time_label(self) -> None:
        """Инициализирует метку, отображающую скорость работы алгоритма поиска"""
        label = QLabel(self)
        label.setFont(QFont("Arial", 12))
        size = QRect(
            self._size.width() // 2,
            self._size.height() // 1.5 + 50,
            self._size.width() // 2.5,
            30,
        )
        label.setGeometry(size)
        self._time_label = label

    def _init_memory_label(self) -> None:
        """Инициализирует метку, отображающую количество потребляемой памяти при поиске"""
        label = QLabel(self)
        label.setFont(QFont("Arial", 12))
        size = QRect(
            self._size.width() // 2,
            self._size.height() // 1.5 + 90,
            self._size.width() // 2.5,
            30,
        )
        label.setGeometry(size)
        self._memory_label = label

    def _init_selected_searcher_label(self) -> None:
        """Инициализирует пояснительную метку для выбора алгоритма поиска"""
        label = QLabel(self)
        text = "Search algorithm"
        label.setFont(QFont("Arial", 12))
        label.setText(text)
        size = QRect(10, self._size.height() // 1.5 + 50, 130, 30)
        label.setGeometry(size)

    def _init_substring_label(self) -> None:
        """Инициализирует пояснительную метку для ввода искомой строки"""
        label = QLabel(self)
        text = "Substring"
        label.setFont(QFont("Arial", 12))
        label.setText(text)
        size = QRect(10, self._size.height() // 1.5 + 90, 130, 30)
        label.setGeometry(size)

    def _init_find_button(self) -> None:
        """Инициализирует кнопку 'Find'"""
        btn = QPushButton(self)
        btn.setFont(QFont("Arial", 12))
        btn.setText("Find")
        size = QRect(
            self._size.width() // 2 - 40, self._size.height() // 1.5 + 140, 80, 40
        )
        btn.setGeometry(size)
        btn.clicked.connect(self._action_push_find_button)

    @pyqtSlot()
    def _action_open_file(self) -> None:
        """Помещает содержимое выбранного файла в соответствующий виджет для просмотра этого содержимого"""
        file_name = QFileDialog.getOpenFileName(self)[0]
        try:
            text = read_file(file_name)
            self._text_viewer.setText(text)
        except FileNotFoundError:
            pass

    @pyqtSlot()
    def _action_push_find_button(self) -> None:
        """Запускает поиск указанной строки в тексте, подсвечивая найденные вхождения"""
        text = self._text_viewer.toPlainText()
        substring = self._substring_input.text()
        searcher_name = self._combo_of_searchers.itemText(
            self._combo_of_searchers.currentIndex()
        )
        searcher = self._searchers_by_name[searcher_name]
        length = len(substring)
        indexes = list(
            map(lambda index: (index, length), searcher.search(text, substring))
        )
        self._high_lighter.highlight_found_occurrences(indexes)


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
            if block_len < start:
                self._cursor += block_len + 1
                self._state = BlockState.PREV_BLOCK_IS_NOT_PROCESSED
                return
            start = max(0, start)
            if block_len - start < count:
                self.setFormat(start, block_len - start, self._format)
                self._cursor += block_len + 1
                self._state = BlockState.PREV_BLOCK_IS_NOT_PROCESSED
                return
            self.setFormat(start, count, self._format)
            self._state = BlockState.PREV_BLOCK_IS_PROCESSED

    def highlight_found_occurrences(self, indexes: list[tuple[int, int]]) -> None:
        """
        Подсвечивает найденные вхождения строки в тексте

        :param indexes: индексы вхождений [(start_index, count), ...]
        """
        self._reset()
        for ind in indexes:
            self._indexes.append(ind)
        self._high_lighter.rehighlight()

    def _reset(self) -> None:
        """Сбрасывает все настройки"""
        self._state = BlockState.PREV_BLOCK_IS_PROCESSED
        self._indexes: deque[tuple[int, int]] = deque()
        self._current_index: Optional[tuple[int, int]] = None
        self._cursor: int = 0
