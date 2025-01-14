import utils
import win32con
import win32api
import pyperclip

from PyQt6.QtCore import Qt
from termcolor import colored
from PyQt6.QtGui import QFont
from win10toast import ToastNotifier
from ollama import chat, ChatResponse
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QLabel, QFrame)

class StyleSheet:
    BUTTON = """
        QPushButton {
            background-color: #2C3E50;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #34495E;
        }
        QPushButton:pressed {
            background-color: #2980B9;
        }
    """

    INPUT = """
        QLineEdit {
            padding: 8px;
            border: 2px solid #BDC3C7;
            border-radius: 4px;
            background-color: #FFFFFF;
        }
        QLineEdit:focus {
            border: 2px solid #3498DB;
        }
    """

class MainWindow(QMainWindow):
    def __init__(self, selected_text: str, close_callback: callable):
        super().__init__()
        self.setWindowTitle("Sagy - AI Assistant")
        self.setGeometry(0, 0, 800, 600)
        self.setStyleSheet("background-color: #ECF0F1; color: #2C3E50; font-size: 20px;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.central_widget.setLayout(self.layout)

        self.selected_text = selected_text

        header = QLabel("Sagy")
        header.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #2C3E50; margin-bottom: 10px;")
        self.layout.addWidget(header)

        self.setup_input_section()

        self.setup_actions_section()

        self.setup_result_section()

        self.close_callback = close_callback

    def setup_input_section(self):
        input_frame = QFrame()
        input_frame.setStyleSheet("QFrame { background-color: white; border-radius: 8px; }")
        input_layout = QVBoxLayout(input_frame)

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Ask anything about the selected text...")
        self.question_input.setStyleSheet(StyleSheet.INPUT)
        self.question_input.setMinimumHeight(40)

        input_button_layout = QHBoxLayout()
        self.ask_button = QPushButton("Ask AI")
        self.ask_button.setStyleSheet(StyleSheet.BUTTON)
        self.ask_button.clicked.connect(self.ask_ai)

        input_button_layout.addWidget(self.question_input)
        input_button_layout.addWidget(self.ask_button)
        input_layout.addLayout(input_button_layout)

        self.layout.addWidget(input_frame)

    def setup_actions_section(self):
        actions_frame = QFrame()
        actions_frame.setStyleSheet("QFrame { background-color: white; border-radius: 8px; padding: 10px; }")
        actions_layout = QVBoxLayout(actions_frame)

        actions_label = QLabel("Quick Actions")
        actions_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        actions_label.setStyleSheet("color: #2C3E50;")
        actions_layout.addWidget(actions_label)

        buttons_layout = QHBoxLayout()

        # Standard actions
        self.proofread_button = QPushButton("🔍 Proofread")
        self.summarize_button = QPushButton("📝 Summarize")

        # New actions
        self.continue_button = QPushButton("🔄 Continue")
        self.simplify_button = QPushButton("📖 Simplify")
        self.format_button = QPushButton("✨ Format")

        for button in [
            self.proofread_button,
            self.summarize_button,
            self.continue_button,
            self.simplify_button,
            self.format_button
        ]:
            button.setStyleSheet(StyleSheet.BUTTON)
            buttons_layout.addWidget(button)

        self.proofread_button.clicked.connect(self.proofread_text)
        self.summarize_button.clicked.connect(self.summarize_text)
        self.continue_button.clicked.connect(self.continue_text)
        self.simplify_button.clicked.connect(self.simplify_text)
        self.format_button.clicked.connect(self.format_text)


        actions_layout.addLayout(buttons_layout)
        self.layout.addWidget(actions_frame)

    def setup_result_section(self):
        result_frame = QFrame()
        result_frame.setStyleSheet("QFrame { background-color: white; border-radius: 8px; }")
        self.result_layout = QVBoxLayout(result_frame)

        result_label = QLabel("Result")
        result_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        result_label.setStyleSheet("color: #2C3E50;")
        self.result_layout.addWidget(result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet(StyleSheet.INPUT)
        self.result_text.setMinimumHeight(60)
        self.result_layout.addWidget(self.result_text)

        button_layout = QHBoxLayout()
        self.copy_button = QPushButton("📋 Copy")
        self.copy_button.setStyleSheet(StyleSheet.BUTTON)
        self.copy_button.clicked.connect(self.copy_result)
        self.copy_button.setVisible(False)
        button_layout.addStretch()
        button_layout.addWidget(self.copy_button)
        self.result_layout.addLayout(button_layout)

        self.layout.addWidget(result_frame)

    def ask_ai(self):
        question = self.question_input.text()
        self.clean_result()
        result = self.infer(f"{question}: '{self.selected_text}'")
        self.result_text.setText(result)
        self.copy_button.setVisible(True)
        self.question_input.setText("")

    def copy_result(self):
        print(colored("Copying result to clipboard.", "green"))
        pyperclip.copy(self.result_text.toPlainText())
        toast = ToastNotifier()

        toast.show_toast(
            "Result Copied!",
            "Your text has been copied to the clipboard.",
            duration=20,
            icon_path="./assets/clipboard.ico",
            threaded=True
        )

    def clean_result(self):
        self.result_text.clear()
        self.copy_button.setVisible(False)

    def proofread_text(self):
        self.clean_result()
        result = self.infer(utils.get_proofread_prompt(self.selected_text))
        self.result_text.setText(result)
        self.copy_button.setVisible(True)
        pyperclip.copy(result)
        self.simulate_paste()

    def summarize_text(self):
        self.clean_result()
        result = self.infer(utils.get_summarize_prompt(self.selected_text))
        self.result_text.setText(result)
        self.copy_button.setVisible(True)

    def continue_text(self):
        self.clean_result()
        result = self.infer(utils.get_continue_prompt(self.selected_text))
        self.result_text.setText(result)
        self.copy_button.setVisible(True)

    def simplify_text(self):
        self.clean_result()
        result = self.infer(utils.get_simplify_prompt(self.selected_text))
        self.result_text.setText(result)
        self.copy_button.setVisible(True)

    def format_text(self):
        self.clean_result()
        result = self.infer(utils.get_format_prompt(self.selected_text))
        self.result_text.setText(result)
        self.copy_button.setVisible(True)

    def simulate_paste(self):
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        win32api.keybd_event(ord('V'), 0, 0, 0)
        win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

    def infer(self, text):
        response: ChatResponse = chat(model=utils.get_model(), messages=[{
            "role": "user",
            "content": text
        }])
        return response.message.content if response.message.content else "Error: AI could not understand the question."

    def closeEvent(self, event):
        self.clean_result()
        if hasattr(self, 'close_callback') and callable(self.close_callback):
            try:
                self.close_callback()  # Call the callback function
            except Exception as e:
                print(f"Error in close_callback: {str(e)}")  # Catch any exceptions and log them
        event.accept()  # Always allow the window to close
