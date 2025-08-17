from typing import List, Dict, Any
from transformers import pipeline

# HF NER with good recall
_HF_NER = None

def load_hf_ner():
    global _HF_NER
    if _HF_NER is None:
        # Compact model; good default. Alternatives:
        # "dslim/bert-base-NER" or "dbmdz/bert-large-cased-finetuned-conll03-english"
        _HF_NER = pipeline("token-classification", model="dslim/bert-base-NER", aggregation_strategy="simple")
    return _HF_NER

def run_hf_ner(text: str) -> List[Dict[str, Any]]:
    ner = load_hf_ner()
    results = ner(text)
    out = []
    for r in results:
        out.append({
            "text": r["word"],
            "label": r["entity_group"],
            "score": float(r["score"]),
            "source": "hf"
        })
    return out

def run_spacy_ner(nlp, doc) -> List[Dict[str, Any]]:
    ents = []
    for ent in doc.ents:
        ents.append({
            "text": ent.text,
            "label": ent.label_,
            "score": 1.0,
            "source": "spacy"
        })
    return ents

def merge_entities(spacy_ents, hf_ents):
    # Simple union by (text, label); could be more sophisticated (span merge, fuzzy)
    seen = set()
    merged = []
    for e in spacy_ents + hf_ents:
        key = (e["text"].lower(), e["label"])
        if key not in seen:
            seen.add(key)
            merged.append(e)
    return merged
