from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class CVEIngestRequest(BaseModel):
    cve_ids: List[str]

class CVEOut(BaseModel):
    cve_id: str
    source: str
    description: Optional[str]
    published: Optional[str]
    last_modified: Optional[str]
    severity: Optional[str]
    cvss_score: Optional[float]
    cvss_vector: Optional[str]
    cwes: List[str] = []
    vendors: List[str] = []
    products: List[str] = []
    entities: List[Dict[str, Any]] = []
    facts: Dict[str, Any] = {}