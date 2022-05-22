import random

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QTextDocument
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMenu, QMenuBar, \
    QTextEdit

from app.model.utils.file_reader import read_file


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Substring searcher')
        self.setGeometry(300, 300, 800, 600)
        self._init_text_box()
        self._init_menu_bar()
        # self._init_high_lighter()

    def _init_text_box(self) -> None:
        self._text_box = QTextEdit(self)
        self._text_box.setReadOnly(True)
        self.setCentralWidget(self._text_box)

    def _init_high_lighter(self) -> None:
        self._high_lighter = SearchHighLight(self._text_box.document())

    def _init_menu_bar(self) -> None:
        self._menu_bar = QMenuBar(self)
        self.setMenuBar(self._menu_bar)

        file_menu = QMenu('&File', self)
        self._menu_bar.addMenu(file_menu)

        file_menu.addAction('&Open', self.action_open_file)

    @pyqtSlot()
    def action_open_file(self):
        file_name = QFileDialog.getOpenFileName(self)[0]
        try:
            self._text_box.setText(read_file(file_name))

            # self._high_lighter.rehighlight()
        except FileNotFoundError:
            print('No such file')


class SearchHighLight(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument):
        super().__init__(parent)
        self._format = QTextCharFormat()
        self._format.setBackground(Qt.green)

    def highlightBlock(self, text: str) -> None:
        count = random.randint(1, 17)
        self.setFormat(0, count, self._format)
