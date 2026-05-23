import re


# =========================================================
# 🔥 PAGE OBJECT BUILDER
# =========================================================

def build_page_objects(pdf_document):

    page_objects = []

    try:

        for page_index in range(len(pdf_document)):

            page = pdf_document[page_index]

            raw_text = page.get_text(
                "text"
            )

            if not isinstance(raw_text, str):
                raw_text = ""

            lines = raw_text.splitlines()

            paragraphs = []

            current_paragraph = []

            for line in lines:

                original_line = line

                if not isinstance(original_line, str):
                    continue

                line = original_line.rstrip()

                # -----------------------------------------
                # PRESERVE BLANK LINE STRUCTURE
                # -----------------------------------------

                if not line.strip():

                    if current_paragraph:

                        paragraphs.append({
                            "text":
                                "\n".join(
                                    current_paragraph
                                ),

                            "line_count":
                                len(current_paragraph),

                            "type":
                                "paragraph"
                        })

                        current_paragraph = []

                    continue

                current_paragraph.append(
                    original_line
                )

            # -----------------------------------------
            # FINAL PARAGRAPH
            # -----------------------------------------

            if current_paragraph:

                paragraphs.append({
                    "text":
                        "\n".join(
                            current_paragraph
                        ),

                    "line_count":
                        len(current_paragraph),

                    "type":
                        "paragraph"
                })

            # -----------------------------------------
            # FOOTNOTE DETECTION
            # -----------------------------------------

            footnotes = []

            for para in paragraphs:

                para_text = para.get(
                    "text",
                    ""
                )

                if re.match(
                    r'^\s*\d+\.\s+',
                    para_text
                ):

                    footnotes.append(
                        para_text
                    )

            page_object = {

                "page_number":
                    page_index + 1,

                "raw_text":
                    raw_text,

                "line_count":
                    len(lines),

                "paragraph_count":
                    len(paragraphs),

                "paragraphs":
                    paragraphs,

                "footnotes":
                    footnotes
            }

            page_objects.append(
                page_object
            )

    except Exception as e:

        print(
            "❌ IMMUTABLE LAYOUT ENGINE ERROR:"
        )

        print(str(e))

    return page_objects


# =========================================================
# 🔥 FLATTEN PAGE TEXT
# =========================================================

def flatten_page_objects(page_objects):

    structured_text = []

    for page in page_objects:

        structured_text.append(
            f"\n\n=== PAGE {page.get('page_number')} ===\n\n"
        )

        for para in page.get(
            "paragraphs",
            []
        ):

            para_text = para.get(
                "text",
                ""
            ).rstrip()

            if para_text:

                structured_text.append(
                    para_text
                )

                structured_text.append("\n\n")

    return "".join(
        structured_text
    ).strip()
