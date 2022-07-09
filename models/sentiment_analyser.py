from transformers import pipeline

# Load pre-trained sentiment analysis model
nlp = pipeline("sentiment-analysis")

# Load pre-trained emotion detection model
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def analyse_sentiment(text):
    result = nlp(text)[0]
    return result['label']

def detect_emotion(text):
    emotions = emotion_model(text)
    return emotions
