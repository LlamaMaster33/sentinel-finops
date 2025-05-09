from textblob import TextBlob

def analyze_sentiment(text: str):
    """
    Returns polarity [-1..1] and subjectivity [0..1].
    """
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity
