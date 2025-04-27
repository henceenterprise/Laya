import os
import zipfile
from datetime import datetime
import gitignore_parser
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal

class ProjectExporter:
    @staticmethod
    def export_project(folder_path: str) -> str:
        """
        Export the selected folder into a .zip file, respecting .gitignore rules.
        Returns the created .zip file path.
        """
        if not os.path.isdir(folder_path):
            raise ValueError("The selected path is not a valid folder.")

        gitignore_path = os.path.join(folder_path, '.gitignore')
        if not os.path.isfile(gitignore_path):
            raise FileNotFoundError("No .gitignore file found in the selected folder.")

        matches = gitignore_parser.parse_gitignore(gitignore_path)

        folder_name = os.path.basename(folder_path.rstrip('/\\'))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        zip_filename = f"{folder_name}_export_{timestamp}.zip"

        parent_folder = os.path.dirname(folder_path)
        zip_path = os.path.join(parent_folder, zip_filename)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                dirs[:] = [d for d in dirs if not matches(os.path.relpath(os.path.join(root, d), folder_path).replace("\\", "/"))]
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, folder_path).replace("\\", "/")
                    if not matches(relative_path) and relative_path != zip_filename:
                        zipf.write(file_path, arcname=relative_path)

        return zip_path

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

def export_project_ui(window):
    """Handles the full UI flow for exporting a project"""
    folder = QFileDialog.getExistingDirectory(window, "Choose the project folder to export")
    if folder:
        window.label.setText("Exporting project...")
        window.export_button.setEnabled(False)
        window.dev_button.setEnabled(False)
        window.pong_button.setEnabled(False)

        window.export_thread = ExportThread(folder)
        window.export_thread.finished.connect(lambda zip_path: on_export_finished(window, zip_path))
        window.export_thread.error.connect(lambda e: on_export_error(window, e))
        window.export_thread.start()

def on_export_finished(window, zip_path):
    window.voice.say("Export completed!")
    QMessageBox.information(window, "Success", f"Project exported to:\n{zip_path}")
    window.label.setText("Export completed successfully!")
    window.export_button.setEnabled(True)
    window.dev_button.setEnabled(True)
    window.pong_button.setEnabled(True)

def on_export_error(window, e):
    window.voice.say("Error during export.")
    QMessageBox.critical(window, "Error", f"Error exporting project:\n{str(e)}")
    window.label.setText("Error during project export.")
    window.export_button.setEnabled(True)
    window.dev_button.setEnabled(True)
    window.pong_button.setEnabled(True)
