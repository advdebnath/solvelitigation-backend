import json

SOURCE = "/var/www/solvelitigation/nlp_service/app/data/generated_legal_dictionary.json"
TARGET = "/var/www/solvelitigation/nlp_service/app/data/legal_corrections.generated.json"

with open(SOURCE) as fp:
    words = json.load(fp)

corrections = {}

RULES = [
    ("judgmen", "judgment"),
    ("governmen", "government"),
    ("appellan", "appellant"),
    ("responden", "respondent"),
    ("ribunal", "tribunal"),
]

for bad, good in RULES:
    if bad in words:
        corrections[bad] = good

with open(TARGET, "w") as fp:
    json.dump(
        corrections,
        fp,
        indent=2,
        ensure_ascii=False
    )

print("CORRECTIONS:", len(corrections))
print("FILE:", TARGET)
