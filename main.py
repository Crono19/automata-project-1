from lexer_ui import LexerUI
from PyQt6.QtWidgets import QApplication
import sys
from parse import Parser
from lexer import Lexer


def main():
    app = QApplication(sys.argv)
    lexer_ui = LexerUI()
    lexer_ui.show()
    sys.exit(app.exec())


main()
