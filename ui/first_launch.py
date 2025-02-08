import ollama
import pycountry

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                          QPushButton, QLabel,
                          QFrame, QComboBox)

class StyleSheet:
    BUTTON = """
        QPushButton {
            background-color: #2C3E50;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #34495E;
        }
        QPushButton:pressed {
            background-color: #2980B9;
        }
    """

    COMBO_BOX = """
        QComboBox {
            padding: 8px;
            border: 2px solid #BDC3C7;
            border-radius: 6px;
            background-color: white;
            min-height: 40px;
            font-size: 14px;
            color: black; /* Ensure text is visible */
        }
        QComboBox QAbstractItemView {
            background: white; /* Dropdown background */
            color: black; /* Dropdown text color */
        }
        QComboBox:focus {
            border: 2px solid #3498DB;
        }
        QComboBox::drop-down {
            border: none;
            padding-right: 10px;
        }
        QComboBox::down-arrow {
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #2C3E50;
            margin-right: 8px;
        }
    """

    LABEL = """
        QLabel {
            color: #2C3E50;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
        }
    """

    FRAME = """
        QFrame {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
        }
    """

class FirstLaunch(QMainWindow):
    def __init__(self, get_started_callback: callable, close_callback: callable):
        self.get_started_callback = get_started_callback
        self.close_callback = close_callback

        super().__init__()
        self.setWindowTitle("Windows Intelligence - AI Assistant")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #ECF0F1;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.central_widget.setLayout(self.layout)

        self.welcome_frame = QFrame()
        self.welcome_frame.setStyleSheet(StyleSheet.FRAME)
        welcome_layout = QVBoxLayout(self.welcome_frame)

        self.welcome_label = QLabel("Welcome to Windows Intelligence!")
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(self.welcome_label)

        self.subtitle_label = QLabel("Let's get started by setting up your preferences")
        self.subtitle_label.setStyleSheet("font-size: 16px; color: #7F8C8D; margin-bottom: 10px;")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(self.subtitle_label)

        self.layout.addWidget(self.welcome_frame)

        self.settings_frame = QFrame()
        self.settings_frame.setStyleSheet(StyleSheet.FRAME)
        settings_layout = QVBoxLayout(self.settings_frame)

        self.model_label = QLabel("Select your AI model")
        self.model_label.setStyleSheet(StyleSheet.LABEL)
        settings_layout.addWidget(self.model_label)

        self.model_combo_box = QComboBox()
        self.model_combo_box.setStyleSheet(StyleSheet.COMBO_BOX)
        settings_layout.addWidget(self.model_combo_box)
        settings_layout.addSpacing(15)

        self.language_label = QLabel("Select your preferred language")
        self.language_label.setStyleSheet(StyleSheet.LABEL)
        settings_layout.addWidget(self.language_label)

        self.language_combo_box = QComboBox()
        self.language_combo_box.setStyleSheet(StyleSheet.COMBO_BOX)
        settings_layout.addWidget(self.language_combo_box)

        self.layout.addWidget(self.settings_frame)

        self.start_button = QPushButton("Get Started")
        self.start_button.setStyleSheet(StyleSheet.BUTTON)
        self.start_button.clicked.connect(lambda: get_started_callback(self.model_combo_box.currentText(), self.language_combo_box.currentText()))
        self.layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self._fetch_models()
        self._fetch_languages()

    def _fetch_models(self):
        try:
            models = ollama.list()
            if 'models' in models:
                for model in models['models']:
                  self.model_combo_box.addItem(model.model)
            else:
                self.model_combo_box.addItem("No models available")
        except Exception as e:
            self.model_combo_box.addItem("Error fetching models")
            print(f"Error: {e}")

    def _fetch_languages(self):
        try:
            for language in sorted(list(pycountry.languages), key=lambda x: x.name):
                self.language_combo_box.addItem(language.name)
        except Exception as e:
            self.language_combo_box.addItem("English")

    def closeEvent(self, event):
        self.close_callback()
        event.accept()
