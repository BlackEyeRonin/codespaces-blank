# robot/brain.py
from robot.speech import SpeechEngine

class RobotBrain:
    """
    Controls robot behavior: reactions + speaking + animations.
    """
    def __init__(self, eyes):
        self.eyes = eyes
        self.speech = SpeechEngine(eyes_controller=eyes)

        # Map logical expression names to available GIFs
        self.expression_map = [
            "neutral", "speaking", "happy", "angry", "confused", "wink",
            "concerned", "sad_disagree", "look_left", "look_right", "lens_reajust"
        ]

    def set_expression(self, name: str):
        """Safely set an expression. Defaults to neutral if missing."""
        if name not in self.expression_map:
            name = "neutral"
        self.eyes.set_expression(name)

    def speak(self, text: str):
        """Speak text while animating speaking GIF."""
        self.speech.speak(text)

    # Predefined reactions
    def react_happy(self):
        self.set_expression("happy")

    def react_angry(self):
        self.set_expression("angry")

    def react_confused(self):
        self.set_expression("concerned")

    def react_wink(self):
        self.set_expression("wink")

    def react_sad_disagree(self):
        self.set_expression("sad_disagree")

    def look_left(self):
        self.set_expression("look_left")

    def look_right(self):
        self.set_expression("look_right")

    def reajust_lens(self):
        self.set_expression("lens_reajust")
