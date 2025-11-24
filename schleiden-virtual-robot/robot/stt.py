# robot/stt.py
import speech_recognition as sr

class SpeechToText:
    def __init__(self, energy_threshold=300):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.mic = sr.Microphone()

    def listen(self):
        """Record one phrase from microphone and return text."""
        try:
            with self.mic as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=6)

            print("🧠 Recognizing...")
            return self.recognizer.recognize_google(audio)

        except sr.WaitTimeoutError:
            return "I didn't hear anything..."
        except sr.UnknownValueError:
            return "Sorry, I didn't understand that."
        except Exception as e:
            return f"Error: {e}"
