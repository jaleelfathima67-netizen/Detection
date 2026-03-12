import joblib  # type: ignore
import re
import string
import nltk  # type: ignore
from nltk.corpus import stopwords  # type: ignore
import os

# Set up paths
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'model.pkl')
vec_path = os.path.join(base_dir, 'vectorizer.pkl')

# Load model
model = joblib.load(model_path)
vec = joblib.load(vec_path)

# Mock cleaning
try:
    nltk.download('stopwords', quiet=True)
    STOP_WORDS = set(stopwords.words('english'))
except:
    STOP_WORDS = set()

def clean(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', ' ', text)
    tokens = [w for w in text.split() if w not in STOP_WORDS]
    return " ".join(tokens)

test_sentences = [
    # --- REAL NEWS SAMPLES ---
    "G7 ministers hold emergency meeting over rising oil prices",
    "NASA's James Webb Telescope discovers water on a distant planet",
    "Global stock markets show steady growth in the third quarter",
    "Apple announces new AI features for iPhone focusing on privacy",
    "Drinking 8 glasses of water a day is essential for hydration",
    
    # --- FAKE NEWS SAMPLES ---
    "The world is flat and NASA is hiding it with CGI images",
    "Scientists discover that drinking bleach can cure any disease instantly",
    "Aliens have taken over the White House and are controlling the President",
    "New law secretly requires all citizens to wear aluminum foil hats",
    "Phones are actually surveillance drones built by birds"
]

print("-" * 100)
print(f"{'VERDICT':<10} | {'CONFIDENCE':<10} | {'NEWS SNIPPET'}")
print("-" * 100)

for s in test_sentences:
    cleaned = clean(s)
    v = vec.transform([cleaned])
    pred = model.predict(v)[0]
    
    # Handle both calibrated and non-calibrated models
    try:
        proba = model.predict_proba(v)[0]
        conf = max(proba) * 100
    except:
        conf = 100.0 # Fallback for non-probabilistic models
        
    label = "REAL" if pred == 0 else "FAKE"
    # Note: In our trainer, we mapped REAL -> 0, FAKE -> 1
    
    print(f"{label:<10} | {conf:>8.1f}%  | {s}")

print("-" * 100)
