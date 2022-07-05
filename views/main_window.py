from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTextEdit, QFileDialog
from models.sentiment_analyzer import analyze_sentiment

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

        self.analyze_button = QPushButton('Analyze Sentiment', self)
        self.analyze_button.clicked.connect(self.on_analyze_clicked)
        self.layout.addWidget(self.analyze_button)

        self.result_label = QLabel('Sentiment Result: ', self)
        self.layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def on_analyze_clicked(self):
        text = self.text_edit.toPlainText()
        sentiment = analyze_sentiment(text)
        self.result_label.setText(f"Sentiment Result: {sentiment}")

    def load_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', "Text files (*.txt);;CSV files (*.csv)")
        if fname:
            with open(fname, 'r') as file:
                data = file.read()
                self.text_edit.setText(data)
