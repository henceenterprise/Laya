from PyQt6.QtCore import QThread
import pyttsx3
import queue

class VoiceThread(QThread):
    def __init__(self, engine, fila):
        super().__init__()
        self.engine = engine
        self.fila = fila
        self.running = True

    def run(self):
        while self.running:
            try:
                texto = self.fila.get(timeout=0.1)
                self.engine.say(texto)
                self.engine.runAndWait()
            except queue.Empty:
                continue

    def parar(self):
        self.running = False

class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        self.queue = queue.Queue()
        self.thread = VoiceThread(self.engine, self.queue)
        self.thread.start()

    def say(self, texto):
        print(f"[Laya diz]: {texto}")
        self.queue.put(texto)

    def stop(self):
        self.thread.parar()
        self.thread.wait()
