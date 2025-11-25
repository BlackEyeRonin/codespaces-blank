# robot/camera_detector.py
import cv2
import threading
import time

class CameraDetector:
    """
    Handles webcam feed and face detection in a separate thread.
    Calls a callback when a person (face) is detected.
    """

    def __init__(self, on_person_detected=None):
        self.on_detect = on_person_detected
        self.running = False
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # auto-detect camera
        self.cam_id = self.get_available_camera()
        if self.cam_id is None:
            print("❌ No camera found.")
            self.cap = None
        else:
            print(f"📷 Using camera ID: {self.cam_id}")
            self.cap = cv2.VideoCapture(self.cam_id)

    def get_available_camera(self):
        """Try camera IDs 0–4 and return the first available."""
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cap.release()
                return i
        return None

    def start(self):
        if not self.cap:
            return
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        detected_before = False
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.2)
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
            )

            person_here = len(faces) > 0

            if person_here and not detected_before:
                detected_before = True
                if self.on_detect:
                    self.on_detect(frame)  # optional frame passed to callback

            if not person_here:
                detected_before = False

            time.sleep(0.25)

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
