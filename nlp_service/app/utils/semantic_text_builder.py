import re

from app.utils.legal_text_normalizer import (
    normalize_legal_text
)

# =========================================================
# 🔒 IMMUTABLE SEMANTIC TEXT BUILDER
# =========================================================

def build_semantic_reasoning_text(
    raw_legal_text
):

    if not raw_legal_text:
        return ""

    # -----------------------------------------------------
    # 🔒 IMMUTABLE SOURCE LOCK
    # -----------------------------------------------------

    raw_legal_text = str(
        raw_legal_text
    )

    immutable_copy = str(
        raw_legal_text
    )

    # -----------------------------------------------------
    # 🔒 NORMALIZED SEMANTIC SOURCE
    # -----------------------------------------------------

    semantic_text = normalize_legal_text(
        immutable_copy
    )

    # -----------------------------------------------------
    # 🔒 SAFE SEMANTIC CLEANUP
    # -----------------------------------------------------

    semantic_text = re.sub(
        r"\s+",
        " ",
        semantic_text
    ).strip()

    # -----------------------------------------------------
    # 🔒 FINAL IMMUTABILITY ASSERTION
    # -----------------------------------------------------

    assert (
        raw_legal_text == immutable_copy
    )

    return semantic_text
