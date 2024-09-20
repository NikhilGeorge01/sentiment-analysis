from flask import Flask, render_template, request
import spacy
import nltk
nltk.download('opinion_lexicon')
from nltk.corpus import opinion_lexicon





app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Define simple positive and negative keywords
positive_words = set(opinion_lexicon.positive())
negative_words = set(opinion_lexicon.negative())

# Simple function to analyze sentiment based on keywords
def analyze_sentiment(text):
    doc = nlp(text)  # Tokenize the text using spaCy
    pos_count = sum([1 for token in doc if token.text.lower() in positive_words])
    neg_count = sum([1 for token in doc if token.text.lower() in negative_words])
    
    if pos_count > neg_count:
        return 'Positive'
    elif neg_count > pos_count:
        return 'Negative'
    else:
        return 'Neutral'

# Home route (input form + result)
@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = ""
    if request.method == "POST":
        user_text = request.form["text"]
        sentiment = analyze_sentiment(user_text)  # Call sentiment analysis function
    return render_template("index.html", sentiment=sentiment)

if __name__ == "__main__":
    app.run(debug=True)
