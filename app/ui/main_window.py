from bs4 import BeautifulSoup
from PyQt5.QtCore import QRect, QSize, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QComboBox, QFileDialog, QInputDialog, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QMessageBox, QPushButton, QTextEdit)

from app.model.searchers.abstract_substring_searcher import \
    AbstractSubstringSearcher
from app.model.searchers.aho_korasik_searcher import AhoKorasikSearcher
from app.model.searchers.boyer_moore_searcher import BoyerMooreSearcher
from app.model.searchers.brute_force_searcher import BruteForceSearcher
from app.model.searchers.kmp_searcher import KMPSearcher
from app.model.searchers.rabin_karp_searcher.rabin_karp_polynomial_hash import \
    RabinKarpWithPolynomialHashSearcher
from app.model.searchers.rabin_karp_searcher.rabin_karp_square_hash import \
    RabinKarpWithSquareHashSearcher
from app.model.utils.file_reader import read_file
from app.model.utils.memory_profiler import MemoryProfiler
from app.model.utils.stopwatch import Stopwatch
from app.model.utils.url_loader import load_content_as_string
from app.ui.high_lighter import HighLighter


class MainWindow(QMainWindow):
    """Класс главного окна GUI"""

    def __init__(self):
        super().__init__()
        self._standard_font = QFont("Arial", 12)
        self._init_searchers_by_name()
        self._init_window()
        self._init_menu_bar()
        self._init_text_viewer()
        self._init_labels()
        self._init_combo_of_searchers()
        self._init_substring_input()
        self._init_find_button()
        self._init_high_lighter()
        self._init_input_dialog()

    @property
    def _current_searcher(self) -> AbstractSubstringSearcher:
        searcher_name = self._combo_of_searchers.itemText(
                self._combo_of_searchers.currentIndex()
                )
        searcher = self._searchers_by_name[searcher_name]
        return searcher

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
        searchers[
            "Rabin Karp (Square Hash)"] = RabinKarpWithSquareHashSearcher()
        searchers["Boyer Moore"] = BoyerMooreSearcher()
        searchers["Aho Korasik"] = AhoKorasikSearcher()
        self._searchers_by_name: dict[
            str, AbstractSubstringSearcher] = searchers

    def _init_window(self) -> None:
        """Инициализирует главное окно"""
        self.setWindowTitle("Substring searcher")
        self._size = QSize(800, 600)
        self.setGeometry(200, 200, self._size.width(), self._size.height())
        self.setFixedSize(self._size)

    def _init_text_viewer(self) -> None:
        """Инициализирует виджет для просмотра содержимого файла"""
        text_viewer = QTextEdit(self)
        text_viewer.setFont(self._standard_font)
        text_viewer.setReadOnly(True)
        size = QRect(
                10, 30, self._size.width() - 20, self._size.height() // 1.5)
        text_viewer.setGeometry(size)
        self._text_viewer = text_viewer

    def _init_menu_bar(self) -> None:
        """Инициализирует меню бар"""
        menu_bar = QMenuBar(self)
        menu_bar.setFont(self._standard_font)
        self.setMenuBar(menu_bar)
        file_menu = QMenu("&Open", self)
        file_menu.setFont(self._standard_font)
        file_menu.addAction("&File", self._action_open_file)
        file_menu.addAction("&URL", self._action_open_url)
        menu_bar.addMenu(file_menu)

    def _init_combo_of_searchers(self) -> None:
        """Инициализирует интерфейс выбора алгоритма поиска"""
        searchers = QComboBox(self)
        size = QRect(150, self._size.height() // 1.5 + 50, 235, 30)
        searchers.setGeometry(size)
        searchers.setFont(self._standard_font)
        for name_of_searcher in self._searchers_by_name.keys():
            searchers.addItem(name_of_searcher)
        self._combo_of_searchers: QComboBox = searchers

    def _init_substring_input(self) -> None:
        """Инициализирует окно для ввода искомой строки"""
        sub_inp = QLineEdit(self)
        sub_inp.setFont(self._standard_font)
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
        """
        Инициализирует метку, отображающую скорость работы алгоритма поиска
        """
        label = QLabel(self)
        label.setFont(self._standard_font)
        size = QRect(
                self._size.width() // 2,
                self._size.height() // 1.5 + 50,
                self._size.width() // 2,
                30,
                )
        label.setGeometry(size)
        self._time_label = label

    def _init_memory_label(self) -> None:
        """
        Инициализирует метку,
        отображающую количество потребляемой памяти при поиске
        """
        label = QLabel(self)
        label.setFont(self._standard_font)
        size = QRect(
                self._size.width() // 2,
                self._size.height() // 1.5 + 90,
                self._size.width() // 2,
                30,
                )
        label.setGeometry(size)
        self._memory_label = label

    def _init_selected_searcher_label(self) -> None:
        """Инициализирует пояснительную метку для выбора алгоритма поиска"""
        label = QLabel(self)
        text = "Search algorithm"
        label.setFont(self._standard_font)
        label.setText(text)
        size = QRect(10, self._size.height() // 1.5 + 50, 130, 30)
        label.setGeometry(size)

    def _init_substring_label(self) -> None:
        """Инициализирует пояснительную метку для ввода искомой строки"""
        label = QLabel(self)
        text = "Substring"
        label.setFont(self._standard_font)
        label.setText(text)
        size = QRect(10, self._size.height() // 1.5 + 90, 130, 30)
        label.setGeometry(size)

    def _init_find_button(self) -> None:
        """Инициализирует кнопку 'Find'"""
        btn = QPushButton(self)
        btn.setFont(self._standard_font)
        btn.setText("Find")
        size = QRect(
                self._size.width() // 2 - 40, self._size.height() // 1.5 + 140,
                80, 40
                )
        btn.setGeometry(size)
        btn.clicked.connect(self._action_push_find_button)

    def _init_input_dialog(self) -> None:
        """Инициализирует всплывающее окно для ввода url"""
        self._input_dialog = QInputDialog(None)
        self._input_dialog.setInputMode(QInputDialog.TextInput)
        self._input_dialog.setWindowTitle("Input URL")
        self._input_dialog.setLabelText("Enter URL:")
        self._input_dialog.setFixedSize(QSize(350, 100))
        self._input_dialog.setFont(self._standard_font)

    @pyqtSlot()
    def _action_open_file(self) -> None:
        """
        Помещает содержимое выбранного файла в соответствующий
        виджет для просмотра этого содержимого
        """
        file_name = QFileDialog.getOpenFileName(self)[0]
        try:
            self._text_viewer.setText(read_file(file_name))
        except:
            self._notify_about_open_text_resource_error()

    @pyqtSlot()
    def _action_open_url(self) -> None:
        """
        Помещает содержимое тэгов <p> и <span> из html указанного url в
        виджет для просмотра текста
        """
        if not self._input_dialog.exec_():
            return
        try:
            raw_html = load_content_as_string(self._input_dialog.textValue())
            tags = BeautifulSoup(raw_html, "html.parser").findAll(
                    ["p", "span"])
            chunks_of_text = filter(
                    lambda text: text, map(lambda tag: tag.text, tags))
            self._text_viewer.setText("\n\n".join(chunks_of_text).strip())
        except Exception:
            self._notify_about_open_text_resource_error()

    def _notify_about_open_text_resource_error(self):
        QMessageBox.about(
                self,
                "Ошибка",
                "Не удалось скопировать текст"
                )

    def _action_push_find_button(self) -> None:
        """
        Запускает поиск указанной строки в тексте,
        подсвечивая найденные вхождения
        """
        string = self._text_viewer.toPlainText()
        if len(string) == 0:
            return
        substring = self._substring_input.text()
        search_result = self._run_searcher(
                self._current_searcher, string, substring)
        self._high_lighter.highlight_found_occurrences(
                search_result, len(substring))

    def _run_searcher(
            self,
            searcher: AbstractSubstringSearcher,
            string: str,
            substring: str) -> list[int]:
        """
        Запускает поисковик подстроки в строке,
        отображая информацию о затратах времени и памяти

        :return: список индексов в строке string,
        где начинается подстрока substring
        """
        stopwatch = Stopwatch()
        memory_profiler = MemoryProfiler()
        stopwatch.start()
        with memory_profiler.profile():
            indexes = searcher.search(string, substring)
        stopwatch.stop()
        self._display_performance_information(stopwatch, memory_profiler)
        return indexes

    def _display_performance_information(
            self,
            stopwatch: Stopwatch,
            memory_profiler: MemoryProfiler
            ) -> None:
        """Отображает информацию о затратах времени и памяти"""
        time = round(stopwatch.get_time_in_seconds(), 3)
        memory = round(
                memory_profiler.get_peak_expended_memory_in_bytes() / 1024, 3)
        self._time_label.setText(f"Время работы: {time} секунд")
        self._memory_label.setText(
                f"Максимальное потребление памяти: {memory} KB")
