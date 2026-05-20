def detect_category(text):
    t = text.lower()

    if "criminal appeal" in t:
        return "Criminal"
    if "civil appeal" in t:
        return "Civil"

    if "ipc" in t:
        return "Criminal"
    if "contract act" in t:
        return "Civil"

    if "service" in t:
        return "Service"
    if "tax" in t or "gst" in t:
        return "Taxation"

    return "Civil"
