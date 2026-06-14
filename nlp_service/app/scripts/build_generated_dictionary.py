from pymongo import MongoClient
from collections import Counter
import json
import re

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["solvelitigation"]

counter = Counter()

for doc in db.judgments.find(
    {},
    {
        "fullText": 1,
        "cleanText": 1,
    }
):
    text = (
        (doc.get("cleanText") or "")
        + " "
        + (doc.get("fullText") or "")
    )

    words = re.findall(
        r"[A-Za-z]{4,}",
        text.lower()
    )

    counter.update(words)

dictionary = {
    word: count
    for word, count in counter.items()
    if count >= 5
}

outfile = (
    "/var/www/solvelitigation/nlp_service/app/data/"
    "generated_legal_dictionary.json"
)

with open(outfile, "w", encoding="utf-8") as fp:
    json.dump(
        dictionary,
        fp,
        indent=2,
        ensure_ascii=False
    )

print("WORDS:", len(dictionary))
print("FILE:", outfile)
