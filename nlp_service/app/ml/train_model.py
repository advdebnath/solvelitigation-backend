import pickle
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"

client = MongoClient(MONGO_URI)
db = client["solvelitigation"]

def extract_outcome(text):
    if not text:
        return None
    t = text.lower()
    if "allowed" in t:
        return 1
    if "dismissed" in t:
        return 0
    return None

def load_data():
    X, y = [], []

    for j in db.judgments.find():
        text = j.get("fullText", "")
        outcome = extract_outcome(text)

        if outcome is not None:
            X.append(text[:2000])
            y.append(outcome)

    return X, y

def train():
    X, y = load_data()

    if len(X) < 5:
        print("❌ Not enough data")
        return

    vectorizer = TfidfVectorizer(max_features=5000)
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vec, y)

    with open("app/ml/model.pkl", "wb") as f:
        pickle.dump((vectorizer, model), f)

    print("✅ Model trained and saved")

if __name__ == "__main__":
    train()
