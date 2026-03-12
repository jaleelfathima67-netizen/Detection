import os
import re
import string
import joblib  # type: ignore
import nltk  # type: ignore
from nltk.corpus import stopwords  # type: ignore

# Ensure NLTK data is available
try:
    nltk.download('stopwords', quiet=True)
    STOP_WORDS = set(stopwords.words('english'))
except Exception:
    STOP_WORDS = set()

def clean_text(text):
    """
    Standardize text by removing punctuation, links, and special characters.
    Numbers are preserved to match the training logic.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', ' ', text)
    tokens = [w for w in text.split() if w not in STOP_WORDS]
    return " ".join(tokens)

def test_model():
    """Load the model and run predictions on sample texts."""
    model_path = 'model.pkl'
    vectorizer_path = 'vectorizer.pkl'
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print(f"Error: Model files not found in {os.getcwd()}")
        print("Please run 'python train_model.py' first.")
        return

    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        print("Model and Vectorizer loaded successfully.\n")
    except Exception as e:
        print(f"Error loading model components: {e}")
        return
    
    # Selection of various news types to test accuracy
    test_texts = [
        "U.S. Secretary of State John F. Kerry said Monday that he will stop in Paris later this week.",
        "The President signed the new infrastructure bill into law today in Washington.",
        "Scientists have discovered that wearing a silver hat protects you from all radio frequencies.",
        "Aliens have established a secret base underwater in the Pacific Ocean according to local fishermen.",
        "Recent breakthroughs in solar panel efficiency are expected to lower electricity costs by 20% by 2027."
    ]
    
    print(f"{'PREDICTION':<10} | {'CONFIDENCE':<10} | {'TEXT PREVIEW'}")
    print("-" * 80)
    
    for text in test_texts:
        cleaned = clean_text(text)
        vec = vectorizer.transform([cleaned])
        
        # Binary prediction (0 = REAL, 1 = FAKE)
        pred = model.predict(vec)[0]
        # Probability scores
        proba = model.predict_proba(vec)[0]
        
        label = "FAKE" if pred == 1 else "REAL"
        confidence = proba[1] if pred == 1 else proba[0]
        
        print(f"{label:<10} | {confidence*100:>9.1f}% | {text[:55]}...")  # type: ignore

if __name__ == "__main__": 
    test_model()  
