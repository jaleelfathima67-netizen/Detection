import os
import re
import string
import joblib
import numpy as np
import nltk
from nltk.corpus import stopwords
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import easyocr
from PIL import Image
import io

# Load paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
VEC_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')
META_PATH = os.path.join(BASE_DIR, 'model_meta.pkl')

# Global variables for models
_model = None
_vectorizer = None
_model_name = "Generic Model"
_reader = None

def get_models(model_type='default'):
    global _vectorizer
    
    # Always load/return the vectorizer
    if _vectorizer is None:
        try:
            _vectorizer = joblib.load(VEC_PATH)
        except Exception as e:
            print(f"Error loading vectorizer: {e}")
            return None, None, "Error"

    # Determine which model file to load
    model_file = MODEL_PATH
    if model_type in ['logistic_regression', 'naive_bayes', 'svm', 'random_forest']:
        specific_path = os.path.join(BASE_DIR, f'model_{model_type}.pkl')
        if os.path.exists(specific_path):
            model_file = specific_path
    
    try:
        model = joblib.load(model_file)
        
        # Determine display name
        if 'logistic_regression' in model_file or model_type == 'logistic_regression':
            name = "Logistic Regression"
        elif 'naive_bayes' in model_file or model_type == 'naive_bayes':
            name = "Multinomial Naive Bayes"
        elif 'svm' in model_file or model_type == 'svm':
            name = "Support Vector Machine (SVM)"
        elif 'random_forest' in model_file or model_type == 'random_forest':
            name = "Random Forest Classifier"
        else:
            name = joblib.load(META_PATH) if os.path.exists(META_PATH) else "Standard Model"
            
        return model, _vectorizer, name
    except Exception as e:
        print(f"Error loading model {model_file}: {e}")
        return None, _vectorizer, "Error Loading Model"

def get_ocr_reader():
    global _reader
    if _reader is None:
        try:
            print("Initializing EasyOCR (this may take a few seconds)...")
            _reader = easyocr.Reader(['en'], gpu=False)
            print("EasyOCR initialized successfully.")
        except Exception as e:
            print(f"Error initializing EasyOCR: {e}")
    return _reader

# Pre-fetch NLTK data
try:
    nltk.download('stopwords', quiet=True)
    STOP_WORDS = set(stopwords.words('english'))
except Exception:
    STOP_WORDS = set()

def clean_text(text):
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

class DetectFakeNews(APIView):
    def post(self, request):
        model_type = request.data.get('model', 'default')
        model, vectorizer, model_name = get_models(model_type)
        if model is None or vectorizer is None:
            return Response({"error": "Model not loaded on server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        text = request.data.get('text', '')
        if not text:
            return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

        cleaned_text = clean_text(text)
        vectorized_text = vectorizer.transform([cleaned_text])
        
        prediction = model.predict(vectorized_text)[0]
        probabilities = model.predict_proba(vectorized_text)[0]
        
        real_prob = float(probabilities[0])
        fake_prob = float(probabilities[1])
        label = "FAKE" if prediction == 1 else "REAL"
        confidence = fake_prob if prediction == 1 else real_prob
        
        return Response({
            "label": label,
            "confidence": round(confidence, 4),
            "real_prob": round(real_prob, 4),
            "fake_prob": round(fake_prob, 4),
            "model_used": model_name,
            "text_preview": text[:100] + "..." if len(text) > 100 else text
        })

class DetectFakeNewsFromImage(APIView):
    def post(self, request):
        model_type = request.data.get('model', 'default')
        model, vectorizer, model_name = get_models(model_type)
        if model is None or vectorizer is None:
            return Response({"error": "Model not loaded on server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        reader = get_ocr_reader()
        if reader is None:
             return Response({"error": "OCR Engine (EasyOCR) not initialized"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read image using PIL to ensure it's valid
            image_content = image_file.read()
            img = Image.open(io.BytesIO(image_content))
            
            # Use EasyOCR to extract text
            results = reader.readtext(image_content, detail=0)
            extracted_text = " ".join(results)
            
            if not extracted_text.strip():
                return Response({
                    "error": "No text could be extracted from the image. Please ensure the image contains clear text.",
                    "label": "UNKNOWN",
                    "confidence": 0,
                    "real_prob": 0,
                    "fake_prob": 0
                }, status=status.HTTP_200_OK)

            cleaned_text = clean_text(extracted_text)
            vectorized_text = vectorizer.transform([cleaned_text])
            
            prediction = model.predict(vectorized_text)[0]
            probabilities = model.predict_proba(vectorized_text)[0]
            
            real_prob = float(probabilities[0])
            fake_prob = float(probabilities[1])
            label = "FAKE" if prediction == 1 else "REAL"
            confidence = fake_prob if prediction == 1 else real_prob
            
            return Response({
                "label": label,
                "confidence": round(confidence, 4),
                "real_prob": round(real_prob, 4),
                "fake_prob": round(fake_prob, 4),
                "extracted_text": extracted_text,
                "model_used": model_name
            })

        except Exception as e:
            return Response({"error": f"Error processing image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)