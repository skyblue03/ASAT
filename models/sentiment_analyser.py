from transformers import pipeline, AutoTokenizer

# Load pre-trained models
nlp = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")

# Load tokenizers
sentiment_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
emotion_tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
ner_tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

def chunk_text(text, tokenizer, chunk_size=512):
    tokens = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=chunk_size)
    for i in range(0, len(tokens['input_ids'][0]), chunk_size):
        chunk = tokens['input_ids'][0][i:i + chunk_size]
        yield tokenizer.decode(chunk, skip_special_tokens=True)

def analyse_sentiment(text):
    sentiments = []
    try:
        for chunk in chunk_text(text, sentiment_tokenizer):
            result = nlp(chunk)[0]
            sentiments.append(result['label'])
        
        # Aggregate results
        sentiment_counts = {sentiment: sentiments.count(sentiment) for sentiment in set(sentiments)}
        most_common_sentiment = max(sentiment_counts, key=sentiment_counts.get)
        return most_common_sentiment
    except Exception as e:
        return f"Error in sentiment analysis: {str(e)}"

def detect_emotion(text, threshold=0.05):
    try:
        emotions = []
        for chunk in chunk_text(text, emotion_tokenizer):
            chunk_emotions = emotion_model(chunk)[0]
            emotions.extend(chunk_emotions)
        significant_emotions = [emotion for emotion in emotions if emotion['score'] > threshold]
        return significant_emotions
    except Exception as e:
        return f"Error in emotion detection: {str(e)}"

def recognize_entities(text):
    try:
        entities = []
        for chunk in chunk_text(text, ner_tokenizer):
            chunk_entities = ner_model(chunk)
            entities.extend(chunk_entities)
        return entities
    except Exception as e:
        return f"Error in entity recognition: {str(e)}"

def generate_pdf_report(data, filename="report.pdf"):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    try:
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 40, "Sentiment Analysis Report")
        c.drawString(100, height - 60, f"Sentiment: {data['sentiment']}")
        c.drawString(100, height - 80, "Emotion Scores:")
        y = height - 100
        for emotion, score in data['emotions'].items():
            c.drawString(100, y, f"{emotion}: {score:.2f}")
            y -= 20
        c.drawString(100, y, "Entities:")
        y -= 20
        for entity in data['entities']:
            c.drawString(100, y, f"{entity['entity_group']}: {entity['word']} (score: {entity['score']:.2f})")
            y -= 20
        c.save()
    except Exception as e:
        print(f"Error in generating PDF report: {str(e)}")

def generate_excel_report(data, filename="report.xlsx"):
    import pandas as pd

    try:
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        df = pd.DataFrame([data['emotions']])
        df.to_excel(writer, index=False, sheet_name='Emotions')
        entities_df = pd.DataFrame(data['entities'])
        entities_df.to_excel(writer, index=False, sheet_name='Entities')
        writer.save()
    except Exception as e:
        print(f"Error in generating Excel report: {str(e)}")
