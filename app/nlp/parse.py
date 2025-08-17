from typing import List, Dict

def extract_svo(doc) -> List[Dict[str, str]]:
    """
    Very simple SVO (subject-verb-object) extraction from spaCy dependencies.
    Useful for "X allows attacker to execute code" style statements.
    """
    svos = []
    for sent in doc.sents:
        subjects = [tok for tok in sent if tok.dep_ in ("nsubj", "nsubjpass")]
        verbs = [tok for tok in sent if tok.pos_ == "VERB"]
        dobjs = [tok for tok in sent if tok.dep_ in ("dobj", "attr", "oprd")]
        if subjects and verbs and dobjs:
            svos.append({
                "subject": subjects[0].text,
                "verb": verbs[0].lemma_,
                "object": dobjs[0].text,
                "sentence": sent.text
            })
    return svos
