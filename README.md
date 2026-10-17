# Final Project

## Emotion Detector — Shayan Nazar

Python and Flask application using IBM Watson NLP EmotionPredict to return
anger, disgust, fear, joy, sadness and the dominant emotion.

Based on the IBM course starter:
https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai

### Run in the Skills Network lab

Place the files in `/home/project/final_project`, then run:

```bash
cd /home/project/final_project
python3 -m pip install -r requirements.txt
python3 test_emotion_detection.py
python3 test_live_emotions.py
python3 -m pylint server.py
python3 server.py
```

Open the lab's application preview on port 5000.

`test_emotion_detection.py` uses explicit HTTP mocks to validate application
logic independently of service availability. `test_live_emotions.py` checks the
five required sentences against the actual Watson service. No local fallback
model substitutes invented scores when Watson is unavailable.

### Evidence status

Local application tests: 8 passed. Pylint server.py: 10.00/10.
Live Watson calls from the build environment returned HTTP 502, so successful
live inference outputs must be captured in the course lab before submission.
