from transformers import pipeline

nlp = pipeline("sentiment-analysis")

def analyse_sentiment(text):
    result = nlp(text)[0]
    return result['label']
