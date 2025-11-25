# robot/speech.py
import pyttsx3
import threading
import queue

class SpeechEngine:
    """
    Thread-safe text-to-speech engine using a dedicated worker thread.
    Prevents pyttsx3 from crashing due to concurrency.
    """
    def __init__(self, eyes_controller=None, rate=170, volume=1.0, voice_id=None):
        self.engine = pyttsx3.init()
        self.eyes = eyes_controller

        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

        if voice_id:
            self.engine.setProperty("voice", voice_id)

        self.queue = queue.Queue()
        self.alive = True

        # Start worker thread
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        """Continuously process speech requests."""
        while self.alive:
            text = self.queue.get()

            if text is None:
                break

            if self.eyes:
                self.eyes.set_expression("speaking")

            self.engine.say(text)
            self.engine.runAndWait()

            if self.eyes:
                self.eyes.set_expression("neutral")

    def speak(self, text: str):
        """Queue speech safely."""
        if not text:
            print("[SpeechEngine] Warning: Empty text.")
            return

        self.queue.put(text)

    def stop(self):
        """Clean shutdown."""
        self.alive = False
        self.queue.put(None)
        self.engine.stop()
