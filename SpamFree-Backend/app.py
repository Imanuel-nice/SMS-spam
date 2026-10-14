from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re

app = Flask(__name__)
CORS(app)  # Enable CORS so your frontend can communicate with this API

# Load trained model and vectorizer at startup
try:
    model = joblib.load('spam_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    print("Model and vectorizer loaded successfully.")
except Exception as e:
    print(f"Error loading model files: {e}. Make sure to run train.py first.")

def extract_signals(text):
    signals = []
    lower_text = text.lower()
    
    if re.search(r'urgent|win|winner|claimed|gift card|valid today|act now', lower_text):
        signals.append('Contains promotional or urgent phrasing')
    if re.search(r'http[s]?://|bit\.ly|tinyurl', lower_text):
        signals.append('Contains external link or shortened URL')
    if re.search(r'\$|\b\d{3,}\b', lower_text):
        signals.append('Contains financial figures or numerical incentives')
        
    if not signals:
        signals.append('No obvious risk indicators found')
        
    return signals

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    message = data['message']
    
    if not message.strip():
        return jsonify({'error': 'Message cannot be empty'}), 400

    # Vectorize and predict
    message_vec = vectorizer.transform([message])
    probability = model.predict_proba(message_vec)[0]  # [prob_ham, prob_spam]
    
    spam_score = round(float(probability[1]) * 100, 2)
    is_spam = spam_score >= 50.0
    
    signals = extract_signals(message)

    response = {
        'message': message,
        'spam_probability': spam_score,
        'verdict': 'SPAM DETECTED' if is_spam else 'LIKELY SAFE',
        'is_spam': is_spam,
        'signals': signals
    }

    return jsonify(response)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'running', 'model_loaded': model is not None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)