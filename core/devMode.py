import os
import subprocess

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
