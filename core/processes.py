import psutil

def is_process_running(name: str) -> bool:
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == name:
            return True
    return False
