from pymongo import MongoClient
from collections import Counter
import json
import re

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["solvelitigation"]

counter = Counter()

for doc in db.judgments.find({}, {"fullText":1,"cleanText":1}):

    text = (
        (doc.get("cleanText") or "")
        + " "
        + (doc.get("fullText") or "")
    )

    counter.update(
        re.findall(
            r"[A-Za-z]{4,}",
            text.lower()
        )
    )

outfile = (
    "/var/www/solvelitigation/nlp_service/app/data/legal_frequency.json"
)

with open(outfile,"w") as fp:
    json.dump(counter, fp)

print("WORDS:", len(counter))
print("FILE:", outfile)
