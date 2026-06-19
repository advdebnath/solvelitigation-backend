"""
Stage 02 Metadata Layer

Orchestrates:

- extract_case_number_bridge()
- extract_court()
- extract_case_type()
- extract_parties()
- extract_judges()
- extract_judgment_date()

This stage does NOT implement extraction logic.

It delegates to dedicated extractor modules.
"""

from app.extractors.case_number_bridge import extract_case_number_bridge
from app.extractors.court_extractor import extract_court
from app.extractors.case_type_extractor import extract_case_type
from app.extractors.party_extractor import extract_parties
from app.extractors.judge_extractor import extract_judges
from app.extractors.date_extractor import extract_judgment_date

from app.utils.case_number_normalizer import (
    normalize_case_number_object
)


def run_stage02_metadata(context):

    raw_header_text = context.get("raw_header_text", "")
    raw_full_text = context.get("raw_full_text", "")
    file_path = context.get("file_path")

    case_number = extract_case_number_bridge(
        raw_header_text
    )

    case_number = normalize_case_number_object(
        case_number
    )

    context["case_number"] = case_number

    if (
        case_number.get("court_type")
        in [
            "SUPREME_COURT",
            "SUPREME COURT"
        ]
    ):
        court_data = {
            "court_type": "SUPREME",
            "court_name": "Supreme Court Of India",
            "court_code": "SC",
            "confidence": 100
        }
    else:
        court_data = extract_court(
            raw_header_text
        )

    context["court_data"] = court_data

    context["case_type_data"] = extract_case_type(
        raw_header_text,
        court=court_data.get("court_name", "")
    )

    context["parties"] = extract_parties(
        raw_header_text
    )

    context["judges"] = extract_judges(
        file_path
    )

    context["judgment_date"] = extract_judgment_date(
        raw_full_text
    )

    return context
