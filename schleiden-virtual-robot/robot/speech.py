# robot/speech.py
import pyttsx3
import threading
import time

class SpeechEngine:
    def __init__(self, eyes_controller=None, rate=170, volume=1.0, voice_id=None):
        self.engine = pyttsx3.init()
        self.eyes = eyes_controller

        # Configure voice settings
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

        # Choose voice if provided
        if voice_id:
            self.engine.setProperty("voice", voice_id)

        # Pyttsx3 is blocking, so we use a thread
        self.lock = threading.Lock()

    def speak(self, text):
        """Speak text while animating robot eyes."""
        def run_tts():
            with self.lock:
                if self.eyes:
                    self.eyes.start_speaking()

                self.engine.say(text)
                self.engine.runAndWait()

                if self.eyes:
                    self.eyes.stop_speaking()

        threading.Thread(target=run_tts, daemon=True).start()
