import json
from rapidfuzz import process

SOURCE = (
    "/var/www/solvelitigation/nlp_service/app/data/"
    "generated_legal_dictionary.json"
)

TARGET = (
    "/var/www/solvelitigation/nlp_service/app/data/"
    "generated_legal_dictionary_clean.json"
)

with open(SOURCE, "r", encoding="utf-8") as fp:
    raw = json.load(fp)

words = set(raw.keys())

clean = {}

for word, freq in raw.items():

    if len(word) < 4:
        continue

    best = process.extractOne(
        word,
        words,
        score_cutoff=95
    )

    clean[word] = freq

with open(
    TARGET,
    "w",
    encoding="utf-8"
) as fp:

    json.dump(
        clean,
        fp,
        indent=2,
        ensure_ascii=False
    )

print("RAW:", len(raw))
print("CLEAN:", len(clean))
print("FILE:", TARGET)
