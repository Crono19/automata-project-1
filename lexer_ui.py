from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTextEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem
from lexer import Lexer


class LexerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Lexer UI')
        self.setGeometry(100, 100, 800, 600)
        
        # Main layout
        main_layout = QVBoxLayout()

        # File open button
        self.btnOpen = QPushButton('Open .txt File', self)
        self.btnOpen.clicked.connect(self.openFileNameDialog)
        main_layout.addWidget(self.btnOpen)

        # Text area
        self.textArea = QTextEdit(self)
        main_layout.addWidget(self.textArea)

        # Process button
        self.btnProcess = QPushButton('Verify Text', self)
        self.btnProcess.clicked.connect(self.processText)
        main_layout.addWidget(self.btnProcess)

        # Layout for tokens table
        self.tokensTable = QTableWidget(self)
        self.tokensTable.setColumnCount(3)
        self.tokensTable.setHorizontalHeaderLabels(['Token', 'Type', 'Count'])
        main_layout.addWidget(self.tokensTable)
        
        # Layout for errors table
        self.errorsTable = QTableWidget(self)
        self.errorsTable.setColumnCount(4)
        self.errorsTable.setHorizontalHeaderLabels(['Error', 'Type', 'Line', 'Column'])
        main_layout.addWidget(self.errorsTable)

        # Set the layout for the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def openFileNameDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a text file", "", "Text Files (*.txt)")
        if fileName:
            with open(fileName, 'r', encoding='utf-8') as file:
                self.textArea.setText(file.read())

    def processText(self):
        text_content = self.textArea.toPlainText()
        if text_content:
            lexer = Lexer(text_content)
            tokens, token_counts = lexer.tokenize()
            self.displayTokenResults(tokens, token_counts)
            self.displayErrorResults(lexer.errors)
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
        