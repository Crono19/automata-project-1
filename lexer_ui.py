from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, \
    QTableWidget, QTableWidgetItem, QLabel
from lexer import Lexer
from parse import Parser
from lexer_in_order import LexerInOrder
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt


class LexerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Lexer and Parser')
        self.setGeometry(100, 100, 800, 600)
        self.applyBackground('fondo_automata.jpg')

        font = QFont('Arial Narrow', 10)
        self.setFont(font)

        # Main layout
        main_layout = QVBoxLayout()

        # Logo
        logo = QLabel(self)
        pixmap = QPixmap('logo.png')
        logo.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        main_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        # File open button
        self.btnOpen = QPushButton('Open .txt File')
        self.styleButton(self.btnOpen)
        self.btnOpen.clicked.connect(self.openFileNameDialog)
        main_layout.addWidget(self.btnOpen)

        # Text area
        self.textArea = QTextEdit()
        main_layout.addWidget(self.textArea)

        # Process button
        self.btnProcess = QPushButton('Verify Text')
        self.styleButton(self.btnProcess)
        self.btnProcess.clicked.connect(self.processText)
        main_layout.addWidget(self.btnProcess)

        # Tokens table
        self.tokensTable = QTableWidget()
        self.tokensTable.setColumnCount(3)
        self.tokensTable.setHorizontalHeaderLabels(['Token', 'Type', 'Count'])
        main_layout.addWidget(self.tokensTable)

        # Lexer errors table
        self.errorsTable = QTableWidget()
        self.errorsTable.setColumnCount(4)
        self.errorsTable.setHorizontalHeaderLabels(['Error', 'Type', 'Line', 'Column'])
        main_layout.addWidget(self.errorsTable)

        # Parsing errors table
        self.parsingErrorsTable = QTableWidget()
        self.parsingErrorsTable.setColumnCount(4)
        self.parsingErrorsTable.setHorizontalHeaderLabels(['Error', 'Type', 'Line', 'Column'])
        main_layout.addWidget(self.parsingErrorsTable)

        # Set the layout for the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def applyBackground(self, imagePath):
        # Ajustar imagen de fondo al tamaño de la ventana
        background = QPixmap(imagePath)
        scaledBackground = background.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        brush = QBrush(scaledBackground)
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, brush)
        self.setPalette(palette)

    def styleButton(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

    def openFileNameDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a text file", "", "Text Files (*.txt)")
        if fileName:
            with open(fileName, 'r', encoding='utf-8') as file:
                self.textArea.setText(file.read())

    def processText(self):
        text_content = self.textArea.toPlainText()
        if text_content:
            lexer = Lexer(text_content)
            lexer_in_order = LexerInOrder(text_content)

            tokens, token_counts = lexer.tokenize()
            tokens_in_order = lexer_in_order.tokenize_in_order()

            for token in tokens_in_order:
                print(token)

            parser = Parser(tokens_in_order)
            
            self.displayTokenResults(tokens, token_counts)
            self.displayErrorResults(lexer.errors)
            try:
                parser.parse()
                print("Parsing completed successfully.")
            except SyntaxError as e:
                self.displayParsingErrorResults(parser.errors)
                print("Error during parsing:")
                print(parser.errors)
                print(e)
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a text file and preview the content first.')

    def displayTokenResults(self, tokens, token_counts):
        # Clear the tokens table
        self.tokensTable.setRowCount(0)

        # Insert token data into the tokens table
        for token, details in token_counts.items():
            if details['type'] != 'ERROR':  # Skip errors
                row_position = self.tokensTable.rowCount()
                self.tokensTable.insertRow(row_position)
                self.tokensTable.setItem(row_position, 0, QTableWidgetItem(token))
                self.tokensTable.setItem(row_position, 1, QTableWidgetItem(details['type']))
                self.tokensTable.setItem(row_position, 2, QTableWidgetItem(str(details['count'])))

        self.tokensTable.resizeColumnsToContents()

    def displayErrorResults(self, errors):
        # Clear the errors table
        self.errorsTable.setRowCount(0)

        # Insert error data into the errors table
        for error in errors:
            row_position = self.errorsTable.rowCount()
            self.errorsTable.insertRow(row_position)
            self.errorsTable.setItem(row_position, 0, QTableWidgetItem(error['value']))
            self.errorsTable.setItem(row_position, 1, QTableWidgetItem(error['type']))
            self.errorsTable.setItem(row_position, 2, QTableWidgetItem(str(error['line'])))
            self.errorsTable.setItem(row_position, 3, QTableWidgetItem(str(error['column'])))

        self.errorsTable.resizeColumnsToContents()

    def addRowToTable(self, value, details):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position, 0, QTableWidgetItem(str(value)))
        self.tableWidget.setItem(row_position, 1, QTableWidgetItem(details['type']))
        self.tableWidget.setItem(row_position, 2, QTableWidgetItem(str(details.get('count', 'N/A'))))
        self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(details['line'])))
        self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(details['column'])))

    def displayParsingErrorResults(self, parsing_errors):
        # Clear the parsing errors table
        self.parsingErrorsTable.setRowCount(0)

        # Insert parsing error data into the table
        for error in parsing_errors:
            row_position = self.parsingErrorsTable.rowCount()
            self.parsingErrorsTable.insertRow(row_position)
            self.parsingErrorsTable.setItem(row_position, 0, QTableWidgetItem(error['value']))
            self.parsingErrorsTable.setItem(row_position, 1, QTableWidgetItem(error['type']))
            self.parsingErrorsTable.setItem(row_position, 2, QTableWidgetItem(str(error['line'])))
            self.parsingErrorsTable.setItem(row_position, 3, QTableWidgetItem(str(error['column'])))

        self.parsingErrorsTable.resizeColumnsToContents()
