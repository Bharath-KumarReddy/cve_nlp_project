import re
import spacy

# lightweight tokenizer/normalizer; keep separate so we can reuse
def load_spacy():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        # If the model wasn't downloaded, raise a clear error
        raise RuntimeError(
            "spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm"
        )

URL_RE = re.compile(r"https?://\S+|www\.\S+")

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = URL_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(nlp, text: str):
    return nlp(text)