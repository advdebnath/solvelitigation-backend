# FILE: nlp_service/section_mapper.py
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

@app.route("/map-sections", methods=["POST"])
def map_sections():
    """
    Compare sections of old vs new Act using TF-IDF cosine similarity.
    """
    data = request.get_json()
    old_sections = data.get("old_sections", [])
    new_sections = data.get("new_sections", [])

    if not old_sections or not new_sections:
        return jsonify({"error": "Missing section data"}), 400

    vectorizer = TfidfVectorizer(stop_words="english")

    old_texts = [s["text"] for s in old_sections]
    new_texts = [s["text"] for s in new_sections]

    all_texts = old_texts + new_texts
    tfidf = vectorizer.fit_transform(all_texts)

    old_vectors = tfidf[:len(old_texts)]
    new_vectors = tfidf[len(old_texts):]

    results = []

    for i, old_sec in enumerate(old_sections):
        similarities = cosine_similarity(old_vectors[i], new_vectors)[0]
        best_match_idx = int(np.argmax(similarities))
        best_score = similarities[best_match_idx]
        new_sec = new_sections[best_match_idx]

        if best_score > 0.25:  # Minimum relevance threshold
            results.append({
                "oldSection": old_sec["section"],
                "newSection": new_sec["section"],
                "similarity": round(float(best_score), 3)
            })

    return jsonify({"matches": results})


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5005, debug=False)
