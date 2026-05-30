import re
from typing import Dict, List

# =========================================================
# 🔥 SEMANTIC JURISPRUDENTIAL CHUNK ENGINE
# =========================================================

ROLE_GROUPS = {
    "FACT": "FACTUAL_MATRIX",
    "FACTS": "FACTUAL_MATRIX",
    "ISSUE": "LEGAL_ISSUES",
    "ARGUMENT": "ARGUMENTS",
    "PRECEDENT": "PRECEDENT_ANALYSIS",
    "RATIO": "RATIO_DECIDENDI",
    "HOLDING": "RATIO_DECIDENDI",
    "OPERATIVE": "OPERATIVE_ORDER",
    "FINAL_ORDER": "OPERATIVE_ORDER",
}


def promote_doctrinal_chunk(current_chunk):

    lower_chunk_text = str(current_chunk.get("text", "")).lower()

    doctrinal_triggers = [
        "we find",
        "therefore",
        "it is held",
        "we hold",
        "we conclude",
        "cannot be permitted",
        "not entitled",
        "high court erred",
        "article 14",
        "article 16",
        "principles of natural justice",
        "equal pay for equal work",
    ]

    if current_chunk.get("chunk_type") == "GENERAL":

        for trigger in doctrinal_triggers:

            if trigger in lower_chunk_text:

                current_chunk["chunk_type"] = "RATIO_DECIDENDI"

                current_chunk["importance"] += 80

                break

    return current_chunk


# =========================================================
# 🔥 BUILD JURISPRUDENTIAL CHUNKS
# =========================================================


def build_jurisprudential_chunks(sentences: List[Dict]) -> List[Dict]:

    if not sentences:
        return []

    chunks = []

    current_chunk = {
        "chunk_id": "C1",
        "chunk_type": "GENERAL",
        "sentences": [],
        "text": "",
        "start_sentence": None,
        "end_sentence": None,
        "importance": 0,
    }

    chunk_counter = 1

    previous_group = None

    for sentence in sentences:

        role = str(sentence.get("role", "GENERAL")).upper()

        group = ROLE_GROUPS.get(role, "GENERAL")

        # -------------------------------------------------
        # START NEW CHUNK
        # -------------------------------------------------

        if previous_group and group != previous_group:

            current_chunk["text"] = " ".join(current_chunk["sentences"])

            current_chunk = promote_doctrinal_chunk(current_chunk)

            chunks.append(current_chunk)

            chunk_counter += 1

            current_chunk = {
                "chunk_id": f"C{chunk_counter}",
                "chunk_type": group,
                "sentences": [],
                "text": "",
                "start_sentence": None,
                "end_sentence": None,
                "importance": 0,
            }

        # -------------------------------------------------
        # ADD SENTENCE
        # -------------------------------------------------

        sentence_text = sentence.get("text", "")

        current_chunk["sentences"].append(sentence_text)

        if current_chunk["start_sentence"] is None:

            current_chunk["start_sentence"] = sentence.get("sentence_id")

        current_chunk["end_sentence"] = sentence.get("sentence_id")

        current_chunk["importance"] += int(sentence.get("weight", 0))

        previous_group = group

    # -----------------------------------------------------
    # FINAL CHUNK
    # -----------------------------------------------------

    if current_chunk["sentences"]:

        current_chunk["text"] = " ".join(current_chunk["sentences"])

        current_chunk = promote_doctrinal_chunk(current_chunk)

        chunks.append(current_chunk)

    return chunks
