from typing import Dict, Any, List
from transformers import pipeline

_zero_shot = None

LABEL_SETS = {
    "impact": [
        "remote code execution", "privilege escalation", "information disclosure",
        "denial of service", "bypass", "sql injection", "xss", "path traversal"
    ],
    "component_type": [
        "library", "web application", "operating system", "firmware",
        "browser", "database", "cloud service"
    ],
    "attack_vector": ["network", "adjacent", "local", "physical"]
}

def load_zero_shot():
    global _zero_shot
    if _zero_shot is None:
        _zero_shot = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    return _zero_shot

def zero_shot_labels(text: str) -> Dict[str, Any]:
    z = load_zero_shot()
    out = {}
    for k, labels in LABEL_SETS.items():
        res = z(text, candidate_labels=labels, multi_label=True)
        out[k] = sorted(
            [{"label": l, "score": float(s)} for l, s in zip(res["labels"], res["scores"])],
            key=lambda x: x["score"],
            reverse=True
        )
    return out

def normalize_severity_from_cvss(score: float | None) -> str | None:
    if score is None:
        return None
    if score >= 9.0:
        return "CRITICAL"
    if score >= 7.0:
        return "HIGH"
    if score >= 4.0:
        return "MEDIUM"
    if score > 0:
        return "LOW"
    return None
