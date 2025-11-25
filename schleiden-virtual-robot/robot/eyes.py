import os
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel


class Eyes:
    """
    Handles animated GIF expressions for the robot.
    Uses QMovie for smooth animations without blocking UI.
    """

    def __init__(self, label: QLabel):
        self.label = label
        self.current_movie = None

        # Path to GIFs
        self.expressions_path = os.path.join("assets", "expressions")

        # Safety
        if self.label:
            self.label.setScaledContents(True)
        else:
            print("[Eyes] ⚠ WARNING: No QLabel provided.")

        # Cache available expressions to avoid repeated disk checks
        self.available = {
            f[:-4] for f in os.listdir(self.expressions_path)
            if f.endswith(".gif")
        }

    def set_expression(self, expression_name: str):
        """
        Switch robot's eyes to a new GIF.
        Falls back to 'neutral' if the GIF doesn't exist.
        """

        # Auto fallback
        if expression_name not in self.available:
            print(f"[Eyes] ⚠ '{expression_name}' not found. Using 'neutral'.")
            expression_name = "neutral"

        gif_path = os.path.join(self.expressions_path, f"{expression_name}.gif")

        # Stop previous animation
        if self.current_movie:
            self.current_movie.stop()

        # Load new GIF
        self.current_movie = QMovie(gif_path)

        if not self.label:
            print("[Eyes] ❌ ERROR: No QLabel to display GIF.")
            return

        self.label.setMovie(self.current_movie)
        self.current_movie.start()

        print(f"[Eyes] ✔ Expression changed → {expression_name}")

    def stop(self):
        """Stop the animation (optional helper)."""
        if self.current_movie:
            self.current_movie.stop()
