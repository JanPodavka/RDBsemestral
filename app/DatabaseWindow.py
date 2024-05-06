from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QApplication, QWidget


class DatabaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label_author = None
        self.layout = None
        self.label_title = None
        self.setWindowTitle("New Window")
        self.setGeometry(0, 0, 300, 150)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.label_title = QLabel("RDBsemestral")
        self.label_title.setStyleSheet("font-size: 24pt; font-weight: bold; color: #333333;")
        self.layout.addWidget(self.label_title)

        self.label_author = QLabel("Authors: Jan Podávka, Ondřej Soukup")
        self.label_author.setStyleSheet("font-size: 12pt; color: #666666;")
        self.layout.addWidget(self.label_author)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def center_window(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

