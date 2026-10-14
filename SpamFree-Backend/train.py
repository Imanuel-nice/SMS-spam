import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

def train_spam_detector():
    print("Loading dataset...")
    # Expects UCI SMS Spam Collection dataset (csv with columns: v1 -> label, v2 -> text)
    try:
        df = pd.read_csv('spam.csv', encoding='latin-1')
        df = df[['v1', 'v2']]
        df.columns = ['label', 'message']
    except FileNotFoundError:
        print("Error: 'spam.csv' not found. Please download the SMS Spam Collection dataset and place it in the root directory.")
        return

    # Encode labels: spam -> 1, ham -> 0
    df['label_num'] = df['label'].map({'spam': 1, 'ham': 0})

    X = df['message']
    y = df['label_num']

    # Split dataset into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Extracting features using TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True, max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training models...")
    # Train Naive Bayes
    nb_model = MultinomialNB()
    nb_model.fit(X_train_vec, y_train)
    nb_pred = nb_model.predict(X_test_vec)
    print(f"Naive Bayes Accuracy: {accuracy_score(y_test, nb_pred) * 100:.2f}%")

    # Train SVM (Support Vector Classifier)
    svm_model = SVC(probability=True, kernel='linear', random_state=42)
    svm_model.fit(X_train_vec, y_train)
    svm_pred = svm_model.predict(X_test_vec)
    print(f"SVM Accuracy: {accuracy_score(y_test, svm_pred) * 100:.2f}%")
    print("\nSVM Classification Report:")
    print(classification_report(y_test, svm_pred))

    # Save the best model (SVM) and vectorizer
    print("Saving model and vectorizer...")
    joblib.dump(svm_model, 'spam_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("Training complete! Model artifacts saved successfully.")

if __name__ == '__main__':
    train_spam_detector()