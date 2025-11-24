import os
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap

class EyesController:
    def __init__(self, label_widget, asset_path="assets/expressions"):
        """
        label_widget = QLabel where the face will display
        """
        self.label = label_widget
        self.path = asset_path

        # Expression map
        self.frames = {
            "neutral": ["neutral.png"],
            "happy": ["happy.png"],
            "concerned": ["concerned.png"],
            "angry": ["angry.png"],
            "speaking": ["speaking_01.png", "speaking_02.png"],
            "blink": ["blink_01.png", "blink_02.png"]
        }

        self.current_expression = "neutral"
        self.current_frame_index = 0

        # Timers
        self.speaking_timer = QTimer()
        self.speaking_timer.timeout.connect(self._animate_speaking)

        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self._blink)
        self.blink_timer.start(3500)  # every ~3.5s

        self.set_expression("neutral")

    # -------------------------------------------------------------------------
    def _set_frame(self, frame_name):
        frame_path = os.path.join(self.path, frame_name)
        pix = QPixmap(frame_path)
        self.label.setPixmap(pix)

    # -------------------------------------------------------------------------
    def set_expression(self, expression):
        """Switch robot facial expression instantly."""
        if expression not in self.frames:
            expression = "neutral"

        self.current_expression = expression
        self.current_frame_index = 0

        frame = self.frames[expression][0]
        self._set_frame(frame)

    # -------------------------------------------------------------------------
    def _blink(self):
        """Handles blink animation automatically."""
        self._set_frame(self.frames["blink"][0])
        QTimer.singleShot(120, lambda: self._set_frame(self.frames["blink"][1]))
        QTimer.singleShot(220, lambda: self.set_expression(self.current_expression))

    # -------------------------------------------------------------------------
    def start_speaking(self):
        """Start mouth/eye animation."""
        self.speaking_timer.start(180)

    # -------------------------------------------------------------------------
    def stop_speaking(self):
        """Stop animation and return to normal mood expression."""
        self.speaking_timer.stop()
        self.set_expression(self.current_expression)

    # -------------------------------------------------------------------------
    def _animate_speaking(self):
        """Cycle between speaking frames."""
        frames = self.frames["speaking"]
        self.current_frame_index = (self.current_frame_index + 1) % len(frames)
        self._set_frame(frames[self.current_frame_index])
