from pymongo import MongoClient
import re

MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"

def get_db():
    return MongoClient(MONGO_URI)["solvelitigation"]

def match_acts(text):
    db = get_db()
    acts = db.actmasters.find()

    matched = []

    for act in acts:
        name = act.get("canonicalName", "")
        aliases = act.get("aliases", [])

        for term in [name] + aliases:
            if re.search(rf"\b{re.escape(term)}\b", text, re.IGNORECASE):
                matched.append(name)
                break

    return list(set(matched))
