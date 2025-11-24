# ui/main_window.py
import os
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

from robot.brain import RobotBrain
from robot.eyes import EyesController

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Schleiden Virtual Robot")
        self.setFixedSize(500, 500)
        self.setStyleSheet("background-color: black;")

        # === Load robot eyes ===
        expressions_path = os.path.join("assets", "expressions")
        self.eyes = EyesController(expressions_path)

        # === Robot brain ===
        self.brain = RobotBrain(self.eyes)

        # === Face Display Widget ===
        self.face_label = QLabel(self)
        self.face_label.setAlignment(Qt.AlignCenter)
        self.face_label.setStyleSheet("background-color: black;")
        self.update_face(self.eyes.get_current_expression())

        # === Buttons ===
        btn_speak = QPushButton("Test Speak")
        btn_speak.clicked.connect(lambda: self.brain.say("Hello! I am Schleiden!"))

        btn_listen = QPushButton("Ask Something")
        btn_listen.clicked.connect(self.handle_listen)

        # === Layout ===
        layout = QVBoxLayout()
        layout.addWidget(self.face_label)
        layout.addWidget(btn_speak)
        layout.addWidget(btn_listen)
        self.setLayout(layout)

        # === Blink Timer ===
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.do_blink)
        self.blink_timer.start(4000)

        # === Camera Detector ===
        self.brain.start_camera(self.on_person_entered)

    def update_face(self, pixmap):
        self.face_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def do_blink(self):
        frame = self.eyes.blink()
        self.update_face(frame)

        QTimer.singleShot(120, lambda: self.update_face(self.eyes.get_current_expression()))

    def on_person_entered(self):
        self.brain.say("Hello! I see you there!")

    def handle_listen(self):
        text = self.brain.listen()
        self.brain.say("You said: " + text)
