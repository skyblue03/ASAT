from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit, QFileDialog, QLabel, QVBoxLayout, QWidget
from models.sentiment_analyser import analyse_sentiment
from .mpl_widget import MplWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Advanced Sentiment Analysis Tool')
        
        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.load_button = QPushButton('Load Text File', self)
        self.load_button.clicked.connect(self.load_file)
        self.layout.addWidget(self.load_button)

        self.load_multiple_button = QPushButton('Load Multiple Files', self)
        self.load_multiple_button.clicked.connect(self.load_multiple_files)
        self.layout.addWidget(self.load_multiple_button)

        self.analyse_button = QPushButton('Analyse Sentiment', self)
        self.analyse_button.clicked.connect(self.on_analyse_clicked)
        self.layout.addWidget(self.analyse_button)

        self.save_button = QPushButton('Save Results', self)
        self.save_button.clicked.connect(self.save_results)
        self.layout.addWidget(self.save_button)

        self.result_label = QLabel('Sentiment Result:', self)
        self.layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def on_analyse_clicked(self):
        text = self.text_edit.toPlainText()
        sentiment = analyse_sentiment(text)
        self.result_label.setText(f"Sentiment Result: {sentiment}")

    def load_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Text files (*.txt);;CSV files (*.csv)")
        if fname:
            with open(fname, 'r') as file:
                data = file.read()
                self.text_edit.setText(data)

    def load_multiple_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Open files', '/home', "Text files (*.txt);;CSV files (*.csv)")
        if files:
            results = []
            for fname in files:
                with open(fname, 'r') as file:
                    data = file.read()
                    sentiment = analyse_sentiment(data)
                    results.append((fname, sentiment))
            result_text = "\n".join(f"{fname}: {sentiment}" for fname, sentiment in results)
            self.text_edit.setText(result_text)

    def save_results(self):
        fname, _ = QFileDialog.getSaveFileName(self, 'Save file', '/home', "Text files (*.txt)")
        if fname:
            with open(fname, 'w') as file:
                data = self.text_edit.toPlainText()
                file.write(data)
