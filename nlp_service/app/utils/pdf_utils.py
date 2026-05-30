import subprocess


def extract_text(pdf_path, html_path=None):
    try:
        print("📄 Extracting PDF:", pdf_path)

        output = subprocess.check_output(["pdftotext", pdf_path, "-"])

        text = output.decode("utf-8")

        if not text.strip():
            print("⚠ WARNING: Empty text from pdftotext")

        return text

    except Exception as e:
        print("❌ Extraction error:", e)
        return ""
