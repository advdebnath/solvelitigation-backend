"""
Stage 05 Persistence Layer

Orchestrates:

- judgment_doc construction
- Mongo persistence
- ingestion updates
- completion workflow
- failure workflow
- publication flags

This stage does NOT implement persistence logic.

It coordinates persistence and workflow services.
"""


def run_stage05_save(context):
    """
    Persistence orchestration stage.

    Future responsibilities:

    - judgment_doc persistence
    - ingestion updates
    - completedAt updates
    - review status persistence
    - failure persistence

    No production logic migrated yet.
    """

    judgment_doc = context.get("judgment_doc")
    review_status = context.get("review_status")
    quality_score = context.get("quality_score")

    context["judgment_doc"] = judgment_doc
    context["review_status"] = review_status
    context["quality_score"] = quality_score

    return context
