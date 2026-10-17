"""Flask deployment for the IBM Watson Emotion Detector.

Static analysis: python -m pylint server.py
"""
from flask import Flask, render_template, request
from requests.exceptions import RequestException
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route('/')
def index():
    """Display the emotion detection interface."""
    return render_template('index.html')


@app.route('/emotionDetector')
def emotion_detector_route():
    """Analyze submitted text and return a readable emotion summary."""
    text_to_analyze = request.args.get('textToAnalyze', '')
    if not text_to_analyze.strip():
        return 'Invalid text! Please try again!'
    try:
        result = emotion_detector(text_to_analyze)
    except (RequestException, ValueError, KeyError, IndexError):
        return 'Emotion service unavailable. Please try again later.', 503
    if result['dominant_emotion'] is None:
        return 'Invalid text! Please try again!'
    scores = ', '.join(
        f"'{emotion}': {result[emotion]}"
        for emotion in ('anger', 'disgust', 'fear', 'joy', 'sadness')
    )
    return (
        f'For the given statement, the system response is {scores}. '
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
