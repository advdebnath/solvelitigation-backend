"""
Stage 02 Metadata Layer

Owns:

- extract_case_number_bridge()
- extract_parties()
- extract_judges()
- extract_judgment_date()

Responsibilities:

- Case identity extraction
- Party extraction
- Judge extraction
- Judgment date extraction

Produces:

- case_number
- petitioner
- respondent
- judges
- judgment_date

Does NOT own:

- category classification
- acts extraction
- section extraction
- points of law
- summaries
- ratio
- operative orders
"""


def run_stage02_metadata(context):
    """
    Future metadata extraction stage.

    Input:
        Stage01 context

    Output:
        Metadata-enriched context
    """
    return context
