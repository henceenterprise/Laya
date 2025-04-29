import pyttsx3
import threading
import queue

class Voice:
    def __init__(self):
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker)
        self.thread.daemon = True
        self.running = True
        self.engine = None  # Moved here, will be initialized inside thread
        self.thread.start()

    def _worker(self):
        # Initialize pyttsx3 inside the worker thread
        self.engine = pyttsx3.init()
        
        while self.running:
            try:
                text = self.queue.get(timeout=0.5)
                if text is None:
                    break
                self.engine.say(text)
                self.engine.runAndWait()
            except queue.Empty:
                continue

        # Clean shutdown
        if self.engine:
            try:
                self.engine.stop()
            except Exception:
                pass

    def say(self, text):
        self.queue.put(text)

    def stop(self):
        self.running = False
        self.queue.put(None)  # Unblocks the worker thread
        if self.thread.is_alive():
            self.thread.join(timeout=2)
