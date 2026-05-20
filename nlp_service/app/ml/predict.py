import pickle

MODEL_PATH = "app/ml/model.pkl"

def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

vectorizer, model = load_model()

def predict(text: str):
    if not text:
        return 50

    vec = vectorizer.transform([text])
    prob = model.predict_proba(vec)[0][1]

    return int(prob * 100)
