"""
Training Script for Scikit-Learn Civic NLP Model.
Run:
    python backend/train_model.py
"""
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from .training_data import TRAINING_SAMPLES


def train_and_save_model(output_dir: str = None) -> str:
    if not output_dir:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, "ai_model")

    os.makedirs(output_dir, exist_ok=True)

    texts, labels = zip(*TRAINING_SAMPLES)

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    X = vectorizer.fit_transform(texts)

    model = MultinomialNB(alpha=0.1)
    model.fit(X, labels)

    model_path = os.path.join(output_dir, "civic_model.pkl")
    vec_path = os.path.join(output_dir, "vectorizer.pkl")

    with open(model_path, "wb") as mf:
        pickle.dump(model, mf)
    with open(vec_path, "wb") as vf:
        pickle.dump(vectorizer, vf)

    print(f"✅ AI Model trained successfully on {len(TRAINING_SAMPLES)} samples!")
    print(f"📦 Model saved to: {model_path}")
    return output_dir


if __name__ == "__main__":
    train_and_save_model()
