from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplWidget(QWidget):
    def __init__(self, parent=None):
        super(MplWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def plot(self, data):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(data.keys(), data.values())
        ax.set_ylabel('Counts')
        ax.set_title('Sentiment Analysis Results')
        self.canvas.draw()
