import random
import datetime
import yaml
from textblob import TextBlob

class RobotBrain:
    def __init__(self, eyes=None, faq_path="data/faq_schleiden.yaml"):
        self.eyes = eyes
        self.mood = "neutral"
        self.faq = self._load_faq(faq_path)

    # -------------------------------------------------------------------------
    def _load_faq(self, path):
        try:
            with open(path, "r") as f:
                return yaml.safe_load(f)
        except:
            return {}

    # -------------------------------------------------------------------------
    def analyze_sentiment(self, text):
        """Determine robot emotion based on user message sentiment."""
        score = TextBlob(text).sentiment.polarity

        if score > 0.3:
            self.mood = "happy"
        elif score < -0.2:
            self.mood = "concerned"
        else:
            self.mood = "neutral"

        if self.eyes:
            self.eyes.set_expression(self.mood)

        return self.mood

    # -------------------------------------------------------------------------
    def reply(self, text):
        """Main AI response engine (simple rule-based + FAQ)."""

        # 1. Sentiment-based emotion
        self.analyze_sentiment(text)

        # 2. FAQ matching
        for q, a in self.faq.items():
            if q.lower() in text.lower():
                return a

        # 3. Generic responses
        responses = {
            "happy": [
                "Aww, that makes me happy too!",
                "You're so kind!",
                "I'm smiling with my pixels!"
            ],
            "neutral": [
                "Hmm, interesting. Tell me more!",
                "Okay! What else do you want to know?",
                "I'm listening carefully."
            ],
            "concerned": [
                "Oh? Everything okay?",
                "That sounds a bit scary...",
                "I'm here for you."
            ]
        }

        return random.choice(responses[self.mood])

    # -------------------------------------------------------------------------
    def start_speaking(self):
        """Animate eyes during speech."""
        if self.eyes:
            self.eyes.start_speaking()

    def stop_speaking(self):
        """Return to mood expression after speech."""
        if self.eyes:
            self.eyes.stop_speaking()
