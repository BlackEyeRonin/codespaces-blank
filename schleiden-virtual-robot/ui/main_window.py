# ui/main_window.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QPushButton, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt
from robot.eyes import Eyes
    from robot.brain import RobotBrain
from robot.camera_detector import CameraDetector
from robot.stt import STTEngine


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Schleiden Virtual Robot")
        self.setGeometry(300, 100, 500, 500)

        # ---------------------- UI LAYOUT ----------------------
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # --- Robot face ----
        self.face_label = QLabel()
        self.face_label.setAlignment(Qt.AlignCenter)
        self.face_label.setFixedSize(300, 300)
        self.main_layout.addWidget(self.face_label)

        # ------------------ ROBOT SETUP ------------------
        self.eyes = Eyes(self.face_label)
        self.brain = RobotBrain(self.eyes)

        # preload
        self.eyes.set_expression("neutral")

        # ------------------ TEXT INPUT -------------------
        self.input_text = QTextEdit()
        self.input_text.setFixedHeight(50)
        self.main_layout.addWidget(self.input_text)

        # SPEAK button
        self.speak_btn = QPushButton("Speak Text")
        self.speak_btn.clicked.connect(self.on_speak)
        self.main_layout.addWidget(self.speak_btn)

        # LISTEN button
        self.listen_btn = QPushButton("Voice Input 🎤")
        self.listen_btn.clicked.connect(self.listen)
        self.main_layout.addWidget(self.listen_btn)

        # ------------------ REACTIONS --------------------
        self.reaction_layout = QHBoxLayout()
        self.main_layout.addLayout(self.reaction_layout)

        for name, method in [
            ("Happy", self.brain.react_happy),
            ("Angry", self.brain.react_angry),
            ("Confused", self.brain.react_confused),
            ("Wink", self.brain.react_wink),
        ]:
            btn = QPushButton(name)
            btn.clicked.connect(method)
            self.reaction_layout.addWidget(btn)

        # ------------------ CAMERA DETECTOR --------------------
        self.camera = CameraDetector(on_person_detected=self.on_person_detected)
        self.camera.start()

        # ------------------ STT ENGINE --------------------
        self.stt = STTEngine()

    # ---------------------- BUTTON FUNCTIONS ----------------------
    def on_speak(self):
        text = self.input_text.toPlainText().strip()
        if text:
            print(f"[UI] Speak: {text}")
            self.brain.speak(text)

    def listen(self):
        """Trigger microphone STT"""
        print("[UI] Starting microphone listening...")

        def callback(text):
            if text:
                print(f"[UI] STT result → {text}")
                self.brain.speak(f"You said: {text}")
            else:
                print("[UI] STT failed")
                self.brain.speak("I didn't catch that.")

        self.stt.listen(callback)

    def on_person_detected(self, frame=None):
        print("[Camera] Person detected!")
        self.brain.react_happy()


# ---------------------- APP START ----------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
