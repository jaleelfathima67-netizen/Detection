import sys
import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Add backend to path to import components
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from train_model import get_model, download_dataset, clean_text, extra_real, extra_fake

def train_all():
    print("="*60)
    print("Initializing Multi-Model Training (Realistic AI Dataset)")
    print("="*60)
    
    # Ensure we are in the root and data is accessible
    data_path = "backend/fake_or_real_news.csv"
    if not os.path.exists(data_path):
        data_path = download_dataset()
    
    if not data_path:
        print("ERROR: Dataset not found and could not be downloaded!")
        return

    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    df['content'] = df['title'].fillna('') + " " + df['text'].fillna('')
    df['label_num'] = df['label'].apply(lambda x: 1 if str(x).strip().upper() == 'FAKE' else 0)
    
    print("Standardizing text content (Cleaning & Normalizing)...")
    df['clean_content'] = [clean_text(t) for t in df['content']]

    # Synthetic data injection for better realism across categories
    print("Injecting synthetic categorical data for improved realism...")
    extra_X_real = pd.Series([clean_text(t) for t in extra_real] * 50)
    extra_y_real = pd.Series([0] * (len(extra_real) * 50))
    extra_X_fake = pd.Series([clean_text(t) for t in extra_fake] * 50)
    extra_y_fake = pd.Series([1] * (len(extra_fake) * 50))

    X = pd.concat([df['clean_content'], extra_X_real, extra_X_fake], ignore_index=True)
    y = pd.concat([df['label_num'], extra_y_real, extra_y_fake], ignore_index=True)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

    print(f"Vectorizing with TF-IDF (10,000 features, Uni/Bi-grams)...")
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7, max_features=10000, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    joblib.dump(vectorizer, 'backend/vectorizer.pkl')
    print("Saved: backend/vectorizer.pkl")

    models_to_train = ['logistic_regression', 'naive_bayes', 'svm', 'random_forest']
    
    for m_type in models_to_train:
        print(f"Training Algorithm: {m_type.replace('_', ' ').title()}...")
        model = get_model(m_type)
        model.fit(X_train_tfidf, y_train)
        joblib.dump(model, f'backend/model_{m_type}.pkl')
        print(f"DONE: Saved model_{m_type}.pkl")

    # Save default model as well
    joblib.dump(model, 'backend/model.pkl')
    print("\n" + "="*60)
    print("ALl REALISTIC AI MODELS TRAINED AND API-READY!")
    print("="*60)

if __name__ == "__main__":
    train_all()
