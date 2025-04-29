import sys
import ctypes
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def set_process_dpi_aware():
    """Ensure the app is DPI-aware before QApplication is created."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # 2 = PROCESS_PER_MONITOR_DPI_AWARE
    except Exception as e:
        print(f"Warning: Could not set DPI awareness. {e}")

def main():
    set_process_dpi_aware()
    
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
