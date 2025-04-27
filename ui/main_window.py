from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from core import Voice, export_project_ui, Ping, is_developer_mode_active, activate_developer_mode, deactivate_developer_mode, toggle_fishing, get_fish_label
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laya Assistant")
        self.resize(320, 320)
        self.position_bottom_right(margin_x=100, margin_y=100)

        icon_path = self.resource_path("assets/favicon/favicon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.voice = Voice()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        dev_frame = QFrame()
        dev_layout = QVBoxLayout(dev_frame)
        dev_label = QLabel("🔧 Developer Mode")
        dev_label.setStyleSheet("font-size: 18px;")
        self.dev_button = QPushButton()
        self.dev_button.clicked.connect(self.toggle_developer_mode)
        dev_layout.addWidget(dev_label)
        dev_layout.addWidget(self.dev_button)

        self.export_button = QPushButton("Export Project (.zip)")
        self.export_button.clicked.connect(self.export_project)
        dev_layout.addWidget(self.export_button)

        layout.addWidget(dev_frame)

        random_frame = QFrame()
        random_layout = QVBoxLayout(random_frame)
        rand_label = QLabel("✨ Random Features")
        rand_label.setStyleSheet("font-size: 18px; color: gray;")
        random_layout.addWidget(rand_label)

        self.pong_button = QPushButton("Ping Laya!")
        self.pong_button.clicked.connect(self.test_ping)
        random_layout.addWidget(self.pong_button)

        self.fishing_mode = False
        self.fish_button = QPushButton(get_fish_label())
        self.fish_button.clicked.connect(self.toggle_fishing)
        random_layout.addWidget(self.fish_button)

        layout.addWidget(random_frame)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.update_developer_state()

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.abspath(relative_path)

    def closeEvent(self, event):
        try:
            if hasattr(self, 'voice') and self.voice:
                self.voice.stop()
        except Exception as e:
            print(f"Error while stopping voice engine: {e}")

        event.accept()

    def update_developer_state(self):
        self.developer_mode = is_developer_mode_active()
        if self.developer_mode:
            self.dev_button.setText("Desativar Developer Mode")
            self.label.setText("Developer mode ativo.")
        else:
            self.dev_button.setText("Ativar Developer Mode")
            self.label.setText("Olá! Sou a Laya 😊")

    def toggle_developer_mode(self):
        if not self.developer_mode:
            activate_developer_mode(self)
        else:
            deactivate_developer_mode(self)

    def export_project(self):
        export_project_ui(self)

    def test_ping(self):
        elapsed_ms = Ping(self.voice)
        self.label.setText(f"Pong! Response time: {elapsed_ms} ms")

    def toggle_fishing(self):
        toggle_fishing(self)

    def position_bottom_right(self, margin_x=100, margin_y=100):
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        window_width = self.width()
        window_height = self.height()

        x = screen_width - window_width - margin_x
        y = screen_height - window_height - margin_y

        self.move(x, y)
