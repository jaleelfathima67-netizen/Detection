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
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', ' ', text)
    tokens = [w for w in text.split() if w not in STOP_WORDS]
    return " ".join(tokens)

test_sentences = [
    "apple is good for health",
    "drinking water is good for health",
    "cpu is the brain of the computer",
    "Donald Trump wins the election in a landslide victory",
    "The world is flat and nasa is lying to everyone"
]

print(f"{'PREDICTION':<10} | {'CONFIDENCE':<10} | {'TEXT'}")
print("-" * 60)

for s in test_sentences:
    cleaned = clean(s)
    v = vec.transform([cleaned])
    pred = model.predict(v)[0]
    proba = model.predict_proba(v)[0]
    label = "FAKE" if pred == 1 else "REAL"
    conf = max(proba) * 100
    print(f"{label:<10} | {conf:>9.1f}% | {s}")
