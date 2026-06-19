"""
Stage 03 Legal Intelligence Layer

Owns:

- extract_points_of_law()
- extract_ratio()
- extract_operative_order()
- classify_category()

Category arbitration:

- infer_category_from_act()
- infer_category_from_sections()
- infer_category_from_case_number()

Responsibilities:

- legal issue extraction
- ratio extraction
- operative order extraction
- category determination
- category conflict resolution

Produces:

- points_of_law
- ratio
- operative_order
- primary_category
- secondary_category
- category_confidence

Does NOT own:

- PDF extraction
- OCR
- metadata extraction
- MongoDB persistence
"""
def run_stage03_legal_intelligence(context):
    """
    Future legal intelligence stage.
    """
    return context
