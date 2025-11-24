import sys
import cv2
import pyttsx3
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, Qt

from analyzer import analyze_drug


# --------------------------------------------------------------------------------
# Camera Detector Thread
# --------------------------------------------------------------------------------
class CameraDetector(QThread):
    person_entered = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True
        self.cam_id = self._get_available_camera()
        self.face = cv2.CascadeClassifier(cv2.data.haarcascades +
                                          "haarcascade_frontalface_default.xml")

    def _get_available_camera(self):
        for cam in range(5):
            c = cv2.VideoCapture(cam)
            if c.isOpened():
                c.release()
                return cam
        return None

    def run(self):
        if self.cam_id is None:
            print("❌ No camera detected.")
            return

        cap = cv2.VideoCapture(self.cam_id)
        seen = False

        while self.running:
            ret, frame = cap.read()
            if not ret:
                self.msleep(200)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face.detectMultiScale(gray, 1.2, 5)

            if len(faces) > 0 and not seen:
                seen = True
                self.person_entered.emit()

            if len(faces) == 0:
                seen = False

            self.msleep(200)

        cap.release()

    def stop(self):
        self.running = False
        self.wait()


# --------------------------------------------------------------------------------
# Virtual Robot GUI
# --------------------------------------------------------------------------------
class RobotUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Schleiden Virtual Robot")
        self.setGeometry(150, 150, 550, 450)

        # --- Speech Engine ---
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)

        # --- Layout ---
        layout = QVBoxLayout()

        self.info_label = QLabel("👁 Waiting for person...")
        self.info_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.info_label, alignment=Qt.AlignCenter)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.analyze_btn = QPushButton("Run Drug Analysis")
        self.analyze_btn.clicked.connect(self.manual_test)
        layout.addWidget(self.analyze_btn)

        self.setLayout(layout)

        # Start camera watcher
        self.cam_thread = CameraDetector()
        self.cam_thread.person_entered.connect(self.greet_person)
        self.cam_thread.start()

    # --------------------------------------------------------------------------------
    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass

    # --------------------------------------------------------------------------------
    def greet_person(self):
        self.output.append("👤 Person detected!\n")
        self.info_label.setText("👋 Hello! I'm active.")
        self.speak("Hello! How can I assist you today?")

    # --------------------------------------------------------------------------------
    def manual_test(self):
        """Dummy test for analyzer (replace with real inputs later)."""
        drug = "paracetamol"
        manu = "cipla"
        mfg = "2024-01-15"
        exp = "2026-01-15"

        result = analyze_drug(drug, manu, mfg, exp)

        self.output.append("---- ANALYSIS RESULT ----\n")
        for key, val in result.items():
            self.output.append(f"{key}: {val}")

        self.speak(f"Result: {result['verdict']}")


# --------------------------------------------------------------------------------
# MAIN APP
# --------------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    ui = RobotUI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
