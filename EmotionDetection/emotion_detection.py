"""Detect five emotions using the IBM Watson NLP runtime."""
import os
import requests

URL = os.getenv(
    'WATSON_EMOTION_URL',
    'https://sn-watson-emotion.labs.skills.network/v1/'
    'watson.runtime.nlp.v1/NlpService/EmotionPredict',
)
HEADERS = {'grpc-metadata-mm-model-id':
           'emotion_aggregated-workflow_lang_en_stock'}
EMOTIONS = ('anger', 'disgust', 'fear', 'joy', 'sadness')


def emotion_detector(text_to_analyze):
    """Return emotion scores and dominant emotion; null scores for bad input."""
    empty = dict.fromkeys((*EMOTIONS, 'dominant_emotion'))
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return empty
    response = requests.post(
        URL, json={'raw_document': {'text': text_to_analyze}},
        headers=HEADERS, timeout=30,
    )
    if response.status_code == 400:
        return empty
    response.raise_for_status()
    scores = response.json()['emotionPredictions'][0]['emotion']
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result['dominant_emotion'] = max(result, key=result.get)
    return result
