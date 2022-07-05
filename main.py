from PyQt5.QtWidgets import QApplication
from views.main_window import MainWindow
import sys

def main():
    app = QApplication(sys.argv)  # Create an application object
    mainWindow = MainWindow()     # Create an instance of your main window class
    mainWindow.show()             # Show the main window
    sys.exit(app.exec_())         # Start the event loop

if __name__ == "__main__":
    main()
