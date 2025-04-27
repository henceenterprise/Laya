import pyttsx3
import threading
import queue

class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker)
        self.thread.daemon = True
        self.running = True
        self.thread.start()

    def _worker(self):
        while self.running:
            try:
                text = self.queue.get(timeout=0.5)
                if text is None:
                    break
                self.engine.say(text)
                self.engine.runAndWait()
            except queue.Empty:
                continue

    def say(self, text):
        self.queue.put(text)

    def stop(self):
        self.running = False
        self.queue.put(None)  # Envia None para desbloquear o queue.get()
        if self.thread.is_alive():
            self.thread.join(timeout=2)  # Espera no máximo 2 segundos
        try:
            self.engine.stop()
        except Exception:
            pass
