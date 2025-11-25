# robot/stt.py
import speech_recognition as sr
import threading

class STTEngine:
    """
    Simple speech-to-text module.
    Listens once, converts speech to text, returns result via callback.
    Runs in a thread so UI never freezes.
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def listen(self, callback):
        """
        Listen once in a background thread.
        When speech is recognized, call: callback(text)
        If failed, callback(None)
        """

        def listen_worker():
            print("[STT] 🎤 Initializing microphone...")
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("[STT] 🔊 Listening...")

                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio)
                    print(f"[STT] ✔ Heard: {text}")
                    callback(text)

                except sr.UnknownValueError:
                    print("[STT] ❌ Didn't understand speech")
                    callback(None)

                except sr.RequestError as e:
                    print(f"[STT] ❌ API Error: {e}")
                    callback(None)

                except Exception as e:
                    print(f"[STT] ❌ Unexpected error: {e}")
                    callback(None)

        # Run without blocking UI
        threading.Thread(target=listen_worker, daemon=True).start()
