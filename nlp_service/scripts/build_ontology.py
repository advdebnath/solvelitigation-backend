from datetime import datetime

from pymongo import MongoClient

from app.services.ontology_canonicalizer import (
    canonicalize_point,
    canonicalize_act
)

from app.data.ontology_blacklist import (
    is_blacklisted
)

client = MongoClient("mongodb://localhost:27017")

db = client["solvelitigation"]

ontology = db["legalontology"]

pipeline = [
    {
        "$match": {
            "pointsOfLaw": {
                "$exists": True,
                "$ne": []
            }
        }
    },
    {
        "$unwind": "$pointsOfLaw"
    },
    {
        "$group": {
            "_id": {
                "$toLower": "$pointsOfLaw.point"
            },
            "frequency": {
                "$sum": 1
            },
            "category": {
                "$first": "$pointsOfLaw.category"
            }
        }
    }
]

count = 0

for item in db.judgments.aggregate(pipeline):

    point = canonicalize_point(item["_id"])

    if not point:
        continue

    if is_blacklisted(point):
        continue

    ontology.update_one(
        {
            "normalizedConcept": point.lower(),
            "ontologyType": "POINT_OF_LAW"
        },
        {
            "$set": {
                "displayName": point,
                "category": item.get("category", "General"),
                "frequency": item["frequency"],
                "ontologyType": "POINT_OF_LAW",
                "updatedAt": datetime.utcnow()
            },
            "$setOnInsert": {
                "createdAt": datetime.utcnow()
            }
        },
        upsert=True
    )

    count += 1

print(f"POINT_OF_LAW NODES CREATED: {count}")

# =====================================================
# ACT ONTOLOGY
# =====================================================

act_pipeline = [
    {
        "$match": {
            "actNames": {
                "$exists": True,
                "$ne": []
            }
        }
    },
    {
        "$unwind": "$actNames"
    },
    {
        "$group": {
            "_id": {
                "$toLower": "$actNames"
            },
            "frequency": {
                "$sum": 1
            }
        }
    }
]

act_count = 0

for item in db.judgments.aggregate(act_pipeline):

    act_name = canonicalize_act(item["_id"])

    if not act_name:
        continue

    if is_blacklisted(act_name):
        continue

    ontology.update_one(
        {
            "normalizedConcept": act_name.lower(),
            "ontologyType": "ACT"
        },
        {
            "$set": {
                "displayName": act_name,
                "category": "ACT",
                "frequency": item["frequency"],
                "ontologyType": "ACT",
                "updatedAt": datetime.utcnow()
            },
            "$setOnInsert": {
                "createdAt": datetime.utcnow()
            }
        },
        upsert=True
    )

    act_count += 1

print(f"ACT NODES CREATED: {act_count}")
