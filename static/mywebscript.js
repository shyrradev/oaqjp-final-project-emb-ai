'use strict';
document.getElementById('emotion-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const output = document.getElementById('system_response');
  const text = document.getElementById('textToAnalyze').value;
  output.textContent = 'Analyzing…';
  try {
    const response = await fetch('/emotionDetector?textToAnalyze=' + encodeURIComponent(text));
    output.textContent = await response.text();
  } catch (error) {
    output.textContent = 'Unable to connect. Please try again.';
  }
});
