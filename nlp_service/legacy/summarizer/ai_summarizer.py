import sys
from transformers import pipeline

# Load your summarization model (change this to your own)
# You can point to a local model path if you've fine-tuned one.
MODEL_PATH = "facebook/bart-large-cnn"  # or "nlp_models/legal-bart-v1"

summarizer = pipeline("summarization", model=MODEL_PATH)

def summarize_text(text: str) -> str:
    """Generate a concise legal summary from input text."""
    try:
        summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
        return summary[0]["summary_text"]
    except Exception as e:
        return f"Error in summarizer: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No text provided", file=sys.stderr)
        sys.exit(1)

    text = sys.argv[1]
    print(summarize_text(text))
