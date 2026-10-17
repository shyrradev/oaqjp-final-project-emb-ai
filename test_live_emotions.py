"""Required live model checks; run inside the Skills Network lab."""
import unittest
from EmotionDetection import emotion_detector


class TestLiveEmotions(unittest.TestCase):
    """Validate the actual Watson predictions for the five course sentences."""
    def test_predictions(self):
        cases = [
            ('I am glad this happened', 'joy'),
            ('I am really mad about this', 'anger'),
            ('I feel disgusted just hearing about this', 'disgust'),
            ('I am so sad about this', 'sadness'),
            ('I am really afraid that this will happen', 'fear'),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(emotion_detector(text)['dominant_emotion'], expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
