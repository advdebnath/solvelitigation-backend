"""
Stage 02 Metadata Layer

Orchestrates:

- extract_case_number_bridge()
- extract_parties()
- extract_judges()
- extract_judgment_date()

This stage does NOT implement extraction logic.

It delegates to dedicated extractor modules.
"""

from app.extractors.case_number_bridge import extract_case_number_bridge
from app.extractors.party_extractor import extract_parties
from app.extractors.judge_extractor import extract_judges
from app.extractors.date_extractor import extract_judgment_date


def run_stage02_metadata(context):

    raw_header_text = context.get("raw_header_text", "")
    raw_full_text = context.get("raw_full_text", "")
    file_path = context.get("file_path")

    context["case_number"] = extract_case_number_bridge(
        raw_header_text
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
