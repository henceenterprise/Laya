from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFrame, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon
from core import ProjectExporter, Voice, open_vs_code, open_fork, close_apps, is_process_running
import time
import sys
import os

class ExportThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(Exception)

    def __init__(self, folder):
        super().__init__()
        self.folder = folder

    def run(self):
        try:
            zip_path = ProjectExporter.export_project(self.folder)
            self.finished.emit(zip_path)
        except Exception as e:
            self.error.emit(e)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Laya Assistant")
        self.resize(320, 240)
        self.position_bottom_right(margin_x=100, margin_y=100)

        # Set window icon (PyInstaller compatible)
        icon_path = self.resource_path("assets/favicon/favicon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.voice = Voice()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Developer Mode
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

        # Random Features
        random_frame = QFrame()
        random_layout = QVBoxLayout(random_frame)
        rand_label = QLabel("✨ Random Features")
        rand_label.setStyleSheet("font-size: 18px; color: gray;")
        random_layout.addWidget(rand_label)

        self.pong_button = QPushButton("Ping Laya!")
        self.pong_button.clicked.connect(self.test_ping)
        random_layout.addWidget(self.pong_button)

        layout.addWidget(random_frame)

        # Status label
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # Initial state
        self.update_developer_state()

    def resource_path(self, relative_path):
        """Get the correct resource path (even when bundled with PyInstaller)"""
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.abspath(relative_path)

    def closeEvent(self, event):
        self.voice.stop()
        super().closeEvent(event)

    def update_developer_state(self):
        self.developer_mode = is_process_running("Code.exe") or is_process_running("Fork.exe")
        if self.developer_mode:
            self.dev_button.setText("Desativar Developer Mode")
            self.label.setText("Developer mode ativo.")
        else:
            self.dev_button.setText("Ativar Developer Mode")
            self.label.setText("Olá! Sou a Laya 😊")

    def toggle_developer_mode(self):
        self.developer_mode = is_process_running("Code.exe") or is_process_running("Fork.exe")

        if not self.developer_mode:
            self.label.setText("Initializing developer mode...")
            self.voice.say("Initializing developer mode")
            self.dev_button.setText("Desativar Developer Mode")
            open_vs_code()
            open_fork()
            self.developer_mode = True
        else:
            self.label.setText("Shutting down developer mode...")
            self.voice.say("Shutting down developer mode")
            self.dev_button.setText("Ativar Developer Mode")
            close_apps()
            self.developer_mode = False

    def export_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Choose the project folder to export")
        if folder:
            self.label.setText("Exporting project...")
            self.export_button.setEnabled(False)
            self.dev_button.setEnabled(False)
            self.pong_button.setEnabled(False)

            self.export_thread = ExportThread(folder)
            self.export_thread.finished.connect(self.on_export_finished)
            self.export_thread.error.connect(self.on_export_error)
            self.export_thread.start()

    def on_export_finished(self, zip_path):
        self.voice.say("Export completed!")
        QMessageBox.information(self, "Success", f"Project exported to:\n{zip_path}")
        self.label.setText("Export completed successfully!")
        self.export_button.setEnabled(True)
        self.dev_button.setEnabled(True)
        self.pong_button.setEnabled(True)

    def on_export_error(self, e):
        self.voice.say("Error during export.")
        QMessageBox.critical(self, "Error", f"Error exporting project:\n{str(e)}")
        self.label.setText("Error during project export.")
        self.export_button.setEnabled(True)
        self.dev_button.setEnabled(True)
        self.pong_button.setEnabled(True)

    def test_ping(self):
        start = time.perf_counter()
        self.voice.say("Pong!")
        end = time.perf_counter()
        elapsed_ms = round((end - start) * 1000, 2)
        self.label.setText(f"Pong! Response time: {elapsed_ms} ms")

    def position_bottom_right(self, margin_x=100, margin_y=100):
        screen_geometry = self.screen().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        window_width = self.width()
        window_height = self.height()

        x = screen_width - window_width - margin_x
        y = screen_height - window_height - margin_y

        self.move(x, y)
