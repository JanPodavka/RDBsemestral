import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet

from app.DatabaseWindow import DatabaseWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RDBsemestral")
        self.setGeometry(0, 0, 400, 200)  # Set window size
        self.center_window()  # Center the window
        self.setStyleSheet("background-color: #f0f0f0;")  # Set background color
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label_title = QLabel("RDBsemestral")
        label_title.setStyleSheet("font-size: 24pt; font-weight: bold; color: #333333;")
        layout.addWidget(label_title)

        label_author = QLabel("Authors: Jan Podávka, Ondřej Soukup")
        label_author.setStyleSheet("font-size: 12pt; color: #666666;")
        layout.addWidget(label_author)

        button_connect = QPushButton("Connect")
        button_connect.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14pt;outline: none;")
        button_connect.clicked.connect(self.open_new_window)
        layout.addWidget(button_connect)

        button_exit = QPushButton("Exit")
        button_exit.setStyleSheet("background-color: #f44336; color: white; font-size: 14pt;outline: none;")
        button_exit.clicked.connect(self.close)
        layout.addWidget(button_exit)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def center_window(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def open_new_window(self):
        new_window = DatabaseWindow()
        new_window.show()


class RDDsemestralApp:
    def __init__(self, argv):
        self.app = QApplication(argv)
        # apply_stylesheet(self.app, theme='dark_cyan.xml')

        self.ui = MainWindow()

    def run(self):
        self.ui.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    RDDGui = RDDsemestralApp(sys.argv)
    RDDGui.run()
