"""
Stage 05 Persistence Layer

Owns:

- judgment_doc construction
- Mongo persistence
- ingestion updates
- completion workflow
- failure workflow
- publication flags

Produces:

- persisted judgment
- ingestion completion state

Does NOT own:

- extraction
- metadata extraction
- legal intelligence
- validation
"""

def run_stage05_save(context):
    return context
