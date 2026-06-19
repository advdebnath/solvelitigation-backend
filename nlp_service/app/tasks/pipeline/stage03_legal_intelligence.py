"""
Stage 03 Legal Intelligence Layer

Orchestrates:

- extract_points_of_law()
- extract_operative_order()
- extract_ratio()

- classify_category()

- infer_category_from_act()
- infer_category_from_sections()
- infer_category_from_case_number()

This stage does NOT implement legal intelligence.

It delegates to dedicated extractor modules.
"""

from app.extractors.point_of_law_extractor import extract_points_of_law
from app.extractors.operative_order_engine import extract_operative_order
from app.extractors.ratio_detector import extract_ratio

from app.extractors.category_classifier import classify_category

from app.services.legal_ontology_service import (
    infer_category_from_act,
    infer_category_from_sections,
    infer_category_from_case_number,
)


def run_stage03_legal_intelligence(context):

    body_text = context.get("body_text", "")
    acts = context.get("acts", {})
    sections = context.get("sections", [])
    case_number = context.get("case_number", {})
    jurisprudential_chunks = context.get(
        "jurisprudential_chunks",
        []
    )

    context["points_of_law"] = extract_points_of_law(
        body_text
    )

    context["ratio"] = extract_ratio(
        body_text,
        jurisprudential_chunks
    )

    context["inferred_act_category"] = (
        infer_category_from_act(
            acts.get("acts", [])
        )
    )

    context["inferred_section_category"] = (
        infer_category_from_sections(
            sections
        )
    )

    context["inferred_case_category"] = (
        infer_category_from_case_number(
            str(case_number)
        )
    )

    return context
