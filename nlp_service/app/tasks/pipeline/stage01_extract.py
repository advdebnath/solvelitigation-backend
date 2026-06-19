def run_stage01_extract(
    *,
    file_path,
    ingestion_id,
):
    """
    Stage 01

    File validation
    PDF extraction
    HTML extraction
    OCR reconstruction
    Semantic reconstruction
    Header/body generation

    Returns context dict.
    """

    context = {
        "ingestion_id": ingestion_id,
        "file_path": file_path,
    }

    return context
