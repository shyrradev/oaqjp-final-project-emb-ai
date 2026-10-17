"""Deterministic unit tests of the Watson adapter and Flask routes.

HTTP responses are mocked; these tests do not claim live model accuracy.
Run test_live_emotions.py in the course lab to verify actual predictions.
"""
import unittest
from unittest.mock import Mock, patch
import requests
from EmotionDetection import emotion_detector
from server import app


class TestEmotionDetector(unittest.TestCase):
    """Verify all five labels, response formatting and error paths."""

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_five_emotions(self, post):
        """Verify extraction for each of the five required sentences."""
        cases = [
            ('I am glad this happened', 'joy'),
            ('I am really mad about this', 'anger'),
            ('I feel disgusted just hearing about this', 'disgust'),
            ('I am so sad about this', 'sadness'),
            ('I am really afraid that this will happen', 'fear'),
        ]
        for text, expected in cases:
            with self.subTest(emotion=expected):
                scores = dict.fromkeys(('anger', 'disgust', 'fear', 'joy', 'sadness'), 0.025)
                scores[expected] = 0.9
                post.return_value = Mock(status_code=200)
                post.return_value.json.return_value = {
                    'emotionPredictions': [{'emotion': scores}]}
                result = emotion_detector(text)
                self.assertEqual(result['dominant_emotion'], expected)
                self.assertEqual(set(result), set(scores) | {'dominant_emotion'})
                self.assertEqual(result[expected], 0.9)
                self.assertEqual(post.call_args.kwargs['json'],
                                 {'raw_document': {'text': text}})

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_status_400(self, post):
        """Watson HTTP 400 returns six None values."""
        post.return_value = Mock(status_code=400)
        self.assertTrue(all(value is None for value in emotion_detector('invalid').values()))

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_blank_input(self, post):
        """Blank inputs are rejected without a network request."""
        for text in ('', '   ', None):
            self.assertIsNone(emotion_detector(text)['dominant_emotion'])
        post.assert_not_called()

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_upstream_error(self, post):
        """HTTP errors are raised for the Flask layer to handle."""
        post.return_value.raise_for_status.side_effect = requests.HTTPError('502')
        with self.assertRaises(requests.HTTPError):
            emotion_detector('Hello')


class TestWebApplication(unittest.TestCase):
    """Verify the actual Flask routes with its test client."""

    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_blank(self):
        response = self.client.get('/emotionDetector?textToAnalyze=')
        self.assertIn(b'Invalid text! Please try again!', response.data)

    @patch('server.emotion_detector')
    def test_formatted_result(self, detector):
        detector.return_value = dict(anger=0.02, disgust=0.01, fear=0.01,
                                     joy=0.94, sadness=0.02, dominant_emotion='joy')
        response = self.client.get('/emotionDetector?textToAnalyze=I+am+happy')
        self.assertIn(b'The dominant emotion is joy.', response.data)

    @patch('server.emotion_detector', side_effect=requests.ConnectionError())
    def test_unavailable(self, _detector):
        response = self.client.get('/emotionDetector?textToAnalyze=Hello')
        self.assertEqual(response.status_code, 503)


if __name__ == '__main__':
    unittest.main(verbosity=2)
