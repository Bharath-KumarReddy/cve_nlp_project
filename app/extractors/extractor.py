from typing import Dict, Any
from app.nlp.preprocess import load_spacy, clean_text, tokenize
from app.nlp.ner import run_spacy_ner, run_hf_ner, merge_entities
from app.nlp.parse import extract_svo
from app.nlp.classify import zero_shot_labels, normalize_severity_from_cvss

_nlp = None
def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = load_spacy()
    return _nlp

def enrich_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Runs NLP on description to extract entities, relations, and labels.
    """
    text = clean_text(rec.get("description") or "")
    if not text:
        rec["entities"] = []
        rec["facts"] = {}
        return rec

    nlp = get_nlp()
    doc = tokenize(nlp, text)

    ents_spacy = run_spacy_ner(nlp, doc)
    ents_hf = run_hf_ner(text)
    entities = merge_entities(ents_spacy, ents_hf)

    svos = extract_svo(doc)
    zs = zero_shot_labels(text)

    # Normalize severity if missing, from cvss score
    if not rec.get("severity"):
        rec["severity"] = normalize_severity_from_cvss(rec.get("cvss_score"))

    rec["entities"] = entities
    rec["facts"] = {
        "svos": svos,
        "zero_shot": zs
    }
    return rec
