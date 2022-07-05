import spacy

# Load the pre-trained spaCy model
nlp = spacy.load('en_core_web_sm')

def analyze_sentiment(text):
    """
    Analyze sentiment of the provided text using spaCy.
    
    Args:
        text (str): Text to analyze.

    Returns:
        str: Sentiment of the text (Positive, Negative, Neutral).
    """
    doc = nlp(text)
    # This is a placeholder for the sentiment analysis logic.
    # You might want to integrate a more advanced sentiment analysis here.
    sentiment = "Neutral"  # Default to neutral for demonstration.
    # Analyze the doc and determine sentiment.
    return sentiment
