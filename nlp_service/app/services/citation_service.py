import re

def extract_judgment_date(text):
    patterns = [
        r"\d{2}-[A-Za-z]{3}-\d{4}",
        r"\d{2}/\d{2}/\d{4}",
        r"\d{4}-\d{2}-\d{2}",
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(0)

    return None


def generate_citation(db, date_str, text):
    year = date_str[-4:] if date_str else "0000"

    t = text.lower()

    if "supreme court" in t:
        prefix = "SLSC"
    elif "high court" in t:
        prefix = "SLHC"
    else:
        prefix = "SLTR"

    volume_doc = db.volumes.find_one({"year": year}) or {
        "year": year,
        "volume": 1,
        "currentPage": 1
    }

    start_page = volume_doc["currentPage"]
    page_count = max(1, len(text) // 3000)
    end_page = start_page + page_count

    if end_page > 900:
        volume_doc["volume"] += 1
        start_page = 1
        end_page = page_count

    db.volumes.update_one(
        {"year": year},
        {"$set": {"volume": volume_doc["volume"], "currentPage": end_page}},
        upsert=True
    )

    citation = f"{year} ({volume_doc['volume']}) {prefix} {start_page}"

    return citation, start_page, end_page, page_count
