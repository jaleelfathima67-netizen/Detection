import os
import joblib
import easyocr
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
VEC_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

print("Starting verification...")

try:
    print(f"Loading model from {MODEL_PATH}...")
    model = joblib.load(MODEL_PATH)
    print("Model loaded.")
    
    print(f"Loading vectorizer from {VEC_PATH}...")
    vectorizer = joblib.load(VEC_PATH)
    print("Vectorizer loaded.")
    
    print("Initializing EasyOCR...")
    reader = easyocr.Reader(['en'], gpu=False)
    print("EasyOCR initialized.")
    
    print("All good!")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
