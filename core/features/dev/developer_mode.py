import os
import subprocess
from core.processes import is_process_running

def open_vs_code():
    try:
        subprocess.Popen(["code"], shell=True)
    except Exception as e:
        return f"Erro ao abrir VS Code: {e}"

def open_fork():
    try:
        fork_path = r"C:\Users\david\AppData\Local\Fork\current\Fork.exe"
        if os.path.exists(fork_path):
            subprocess.Popen([fork_path], shell=True)
        else:
            return "Fork.exe não encontrado no caminho definido."
    except Exception as e:
        return f"Erro ao abrir Fork: {e}"

def close_apps():
    os.system("taskkill /f /im Code.exe")
    os.system("taskkill /f /im Fork.exe")

def is_developer_mode_active():
    return is_process_running("Code.exe") or is_process_running("Fork.exe")

def activate_developer_mode(window):
    window.label.setText("Initializing developer mode...")
    window.voice.say("Initializing developer mode")
    window.dev_button.setText("Desativar Developer Mode")
    open_vs_code()
    open_fork()
    window.developer_mode = True

def deactivate_developer_mode(window):
    window.label.setText("Shutting down developer mode...")
    window.voice.say("Shutting down developer mode")
    window.dev_button.setText("Ativar Developer Mode")
    close_apps()
    window.developer_mode = False
