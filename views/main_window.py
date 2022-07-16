from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit, QFileDialog, QLabel, QVBoxLayout, QWidget, QCheckBox
from PyQt5.QtCore import Qt
from models.sentiment_analyser import analyse_sentiment, detect_emotion, recognize_entities, generate_pdf_report, generate_excel_report, track_sentiment_trends
from .mpl_widget import MplWidget
from datetime import datetime
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import contractions

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Advanced Sentiment Analysis Tool')
        
        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.textChanged.connect(self.on_text_changed)
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

        self.emotion_button = QPushButton('Detect Emotions', self)
        self.emotion_button.clicked.connect(self.on_detect_emotion_clicked)
        self.layout.addWidget(self.emotion_button)

        self.entity_button = QPushButton('Recognize Entities', self)
        self.entity_button.clicked.connect(self.on_recognize_entities_clicked)
        self.layout.addWidget(self.entity_button)

        self.real_time_checkbox = QCheckBox('Enable Real-time Analysis', self)
        self.real_time_checkbox.stateChanged.connect(self.on_real_time_checkbox_changed)
        self.layout.addWidget(self.real_time_checkbox)

        self.track_trends_button = QPushButton('Track Sentiment Trends', self)
        self.track_trends_button.clicked.connect(self.on_track_trends_clicked)
        self.layout.addWidget(self.track_trends_button)

        self.remove_punctuation_checkbox = QCheckBox('Remove Punctuation', self)
        self.remove_punctuation_checkbox.stateChanged.connect(self.on_preprocessing_option_changed)
        self.layout.addWidget(self.remove_punctuation_checkbox)

        self.lowercase_checkbox = QCheckBox('Convert to Lowercase', self)
        self.lowercase_checkbox.stateChanged.connect(self.on_preprocessing_option_changed)
        self.layout.addWidget(self.lowercase_checkbox)

        self.remove_stopwords_checkbox = QCheckBox('Remove Stopwords', self)
        self.remove_stopwords_checkbox.stateChanged.connect(self.on_preprocessing_option_changed)
        self.layout.addWidget(self.remove_stopwords_checkbox)

        self.remove_urls_checkbox = QCheckBox('Remove URLs', self)
        self.remove_urls_checkbox.stateChanged.connect(self.on_preprocessing_option_changed)
        self.layout.addWidget(self.remove_urls_checkbox)

        self.remove_mentions_checkbox = QCheckBox('Remove Mentions', self)
        self.remove_mentions_checkbox.stateChanged.connect(self.on_preprocessing_option_changed)
        self.layout.addWidget(self.remove_mentions_checkbox)

        self.remove_hashtags_checkbox = QCheckBox('Remove Hashtags', self)
        self.remove_hashtags_checkbox.stateChanged.connect(self.on_preprocessing_option_changed)
        self.layout.addWidget(self.remove_hashtags_checkbox)

        self.remove_numbers_checkbox = QCheckBox('Remove Numbers', self)
        self.remove_numbers_checkbox.stateChanged.connect(self.on_preprocessing_option_changed)
        self.layout.addWidget(self.remove_numbers_checkbox)

        self.expand_contractions_checkbox = QCheckBox('Expand Contractions', self)
        self.expand_contractions_checkbox.stateChanged.connect(self.on_preprocessing_option_changed)
        self.layout.addWidget(self.expand_contractions_checkbox)

        self.remove_whitespace_checkbox = QCheckBox('Remove Excess Whitespace', self)
        self.remove_whitespace_checkbox.stateChanged.connect(self.on_preprocessing_option_changed)
        self.layout.addWidget(self.remove_whitespace_checkbox)

        self.lemmatization_checkbox = QCheckBox('Lemmatisation', self)
        self.lemmatization_checkbox.stateChanged.connect(self.on_preprocessing_option_changed)
        self.layout.addWidget(self.lemmatization_checkbox)

        self.save_pdf_button = QPushButton('Save PDF Report', self)
        self.save_pdf_button.clicked.connect(self.on_save_pdf_report_clicked)
        self.layout.addWidget(self.save_pdf_button)

        self.save_excel_button = QPushButton('Save Excel Report', self)
        self.save_excel_button.clicked.connect(self.on_save_excel_report_clicked)
        self.layout.addWidget(self.save_excel_button)

        self.result_label = QLabel('Sentiment Result:', self)
        self.layout.addWidget(self.result_label)

        self.emotion_label = QLabel('Emotion Detection Result:', self)
        self.layout.addWidget(self.emotion_label)

        self.entity_label = QLabel('Entity Recognition Result:', self)
        self.layout.addWidget(self.entity_label)

        self.mpl_widget = MplWidget(self)
        self.layout.addWidget(self.mpl_widget)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.current_sentiment = None
        self.current_emotions = None
        self.current_entities = None
        self.real_time_analysis_enabled = False
        self.texts = []
        self.dates = []

        self.preprocessing_options = {
            'remove_punctuation': False,
            'convert_to_lowercase': False,
            'remove_stopwords': False,
            'remove_urls': False,
            'remove_mentions': False,
            'remove_hashtags': False,
            'remove_numbers': False,
            'expand_contractions': False,
            'remove_whitespace': False,
            'lemmatization': False
        }

    def on_text_changed(self):
        if self.real_time_analysis_enabled:
            text = self.text_edit.toPlainText()
            self.perform_real_time_analysis(text)

    def on_real_time_checkbox_changed(self, state):
        self.real_time_analysis_enabled = state == Qt.Checked
        if self.real_time_analysis_enabled:
            self.on_text_changed()

    def on_preprocessing_option_changed(self, state):
        sender = self.sender()
        if sender == self.remove_punctuation_checkbox:
            self.preprocessing_options['remove_punctuation'] = state == Qt.Checked
        elif sender == self.lowercase_checkbox:
            self.preprocessing_options['convert_to_lowercase'] = state == Qt.Checked
        elif sender == self.remove_stopwords_checkbox:
            self.preprocessing_options['remove_stopwords'] = state == Qt.Checked
        elif sender == self.remove_urls_checkbox:
            self.preprocessing_options['remove_urls'] = state == Qt.Checked
        elif sender == self.remove_mentions_checkbox:
            self.preprocessing_options['remove_mentions'] = state == Qt.Checked
        elif sender == self.remove_hashtags_checkbox:
            self.preprocessing_options['remove_hashtags'] = state == Qt.Checked
        elif sender == self.remove_numbers_checkbox:
            self.preprocessing_options['remove_numbers'] = state == Qt.Checked
        elif sender == self.expand_contractions_checkbox:
            self.preprocessing_options['expand_contractions'] = state == Qt.Checked
        elif sender == self.remove_whitespace_checkbox:
            self.preprocessing_options['remove_whitespace'] = state == Qt.Checked
        elif sender == self.lemmatization_checkbox:
            self.preprocessing_options['lemmatization'] = state == Qt.Checked

    def preprocess_text(self, text):
        if self.preprocessing_options['remove_urls']:
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        if self.preprocessing_options['remove_mentions']:
            text = re.sub(r'@\w+', '', text)
        if self.preprocessing_options['remove_hashtags']:
            text = re.sub(r'#\w+', '', text)
        if self.preprocessing_options['remove_numbers']:
            text = re.sub(r'\d+', '', text)
        if self.preprocessing_options['expand_contractions']:
            text = contractions.fix(text)
        if self.preprocessing_options['remove_punctuation']:
            text = re.sub(r'[^\w\s]', '', text)
        if self.preprocessing_options['convert_to_lowercase']:
            text = text.lower()
        if self.preprocessing_options['remove_stopwords']:
            stop_words = set(stopwords.words('english'))
            text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
        if self.preprocessing_options['remove_whitespace']:
            text = ' '.join(text.split())
        if self.preprocessing_options['lemmatization']:
            lemmatizer = WordNetLemmatizer()
            text = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(text)])
        return text

    def perform_real_time_analysis(self, text):
        text = self.preprocess_text(text)
        sentiment = analyse_sentiment(text)
        self.result_label.setText(f"Sentiment Result: {sentiment}")
        self.current_sentiment = sentiment

        emotions = detect_emotion(text)
        if isinstance(emotions, str):
            self.emotion_label.setText(emotions)
        else:
            emotion_result = "\n".join([f"{emotion['label']}: {emotion['score']:.2f}" for emotion in emotions])
            self.emotion_label.setText(f"Emotion Detection Result:\n{emotion_result}")
            self.current_emotions = {emotion['label']: emotion['score'] for emotion in emotions}

        entities = recognize_entities(text)
        if isinstance(entities, str):
            self.entity_label.setText(entities)
        else:
            entity_result = "\n".join([f"{entity['entity_group']}: {entity['word']} (score: {entity['score']:.2f})" for entity in entities])
            self.entity_label.setText(f"Entity Recognition Result:\n{entity_result}")
            self.current_entities = [{'entity_group': entity['entity_group'], 'word': entity['word'], 'score': entity['score']} for entity in entities]

    def on_analyse_clicked(self):
        text = self.text_edit.toPlainText()
        self.perform_real_time_analysis(text)

    def on_detect_emotion_clicked(self):
        text = self.text_edit.toPlainText()
        text = self.preprocess_text(text)
        emotions = detect_emotion(text)
        if isinstance(emotions, str):
            self.emotion_label.setText(emotions)
        else:
            emotion_result = "\n".join([f"{emotion['label']}: {emotion['score']:.2f}" for emotion in emotions])
            self.emotion_label.setText(f"Emotion Detection Result:\n{emotion_result}")
            self.current_emotions = {emotion['label']: emotion['score'] for emotion in emotions}

    def on_recognize_entities_clicked(self):
        text = self.text_edit.toPlainText()
        text = self.preprocess_text(text)
        entities = recognize_entities(text)
        if isinstance(entities, str):
            self.entity_label.setText(entities)
        else:
            entity_result = "\n".join([f"{entity['entity_group']}: {entity['word']} (score: {entity['score']:.2f})" for entity in entities])
            self.entity_label.setText(f"Entity Recognition Result:\n{entity_result}")
            self.current_entities = [{'entity_group': entity['entity_group'], 'word': entity['word'], 'score': entity['score']} for entity in entities]

    def on_save_pdf_report_clicked(self):
        data = {
            'sentiment': self.current_sentiment,
            'emotions': self.current_emotions,
            'entities': self.current_entities
        }
        fname, _ = QFileDialog.getSaveFileName(self, 'Save PDF Report', '', "PDF files (*.pdf)")
        if fname:
            generate_pdf_report(data, fname)

    def on_save_excel_report_clicked(self):
        data = {
            'sentiment': self.current_sentiment,
            'emotions': self.current_emotions,
            'entities': self.current_entities
        }
        fname, _ = QFileDialog.getSaveFileName(self, 'Save Excel Report', '', "Excel files (*.xlsx)")
        if fname:
            generate_excel_report(data, fname)

    def load_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Text files (*.txt);;CSV files (*.csv)")
        if fname:
            with open(fname, 'r') as file:
                data = file.read()
                self.text_edit.setText(data)
                if self.real_time_analysis_enabled:
                    self.perform_real_time_analysis(data)

    def load_multiple_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Open files', '', "Text files (*.txt);;CSV files (*.csv)")
        if files:
            results = []
            for fname in files:
                with open(fname, 'r') as file:
                    data = file.read()
                    sentiment = analyse_sentiment(data)
                    results.append((fname, sentiment))
            result_text = "\n".join(f"{fname}: {sentiment}" for fname, sentiment in results)
            self.text_edit.setText(result_text)

    def on_track_trends_clicked(self):
        texts = self.texts
        dates = self.dates
        texts.append(self.text_edit.toPlainText())
        dates.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        track_sentiment_trends(texts, dates)

    def save_results(self):
        fname, _ = QFileDialog.getSaveFileName(self, 'Save file', '', "Text files (*.txt)")
        if fname:
            with open(fname, 'w') as file:
                data = self.text_edit.toPlainText()
                file.write(data)

    def update_plot(self, data):
        self.mpl_widget.plot(data)
