import os
import subprocess
import tempfile


def repair_pdf(input_path: str) -> str:
    """
    Repairs a PDF using mutool clean.
    Returns repaired file path.
    If repair fails, returns original file.
    """
    try:
        repaired_fd, repaired_path = tempfile.mkstemp(suffix=".pdf")
        os.close(repaired_fd)

        result = subprocess.run(
            ["mutool", "clean", "-d", "-i", input_path, repaired_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
        )

        if result.returncode == 0 and os.path.exists(repaired_path):
            print(f"🛠 PDF repaired successfully: {input_path}")
            return repaired_path
        else:
            print(f"⚠️ Repair failed. Using original PDF: {input_path}")
            return input_path

    except Exception as e:
        print(f"❌ PDF repair exception: {e}")
        return input_path
