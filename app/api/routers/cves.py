from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import SessionLocal
from app.schemas import CVEOut, CVEIngestRequest
from app.models import CVERecord
from app.services.search import search_cves
from app.services.ingest import ingest_cves

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=List[CVEOut])
def list_cves(
    q: Optional[str] = None,
    severity: Optional[str] = None,
    year: Optional[int] = None,
    limit: int = Query(10, le=100),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    rows, total = search_cves(db, q=q, severity=severity, year=year, limit=limit, offset=offset)
    return [CVEOut(**r.to_dict()) for r in rows]

@router.get("/{cve_id}", response_model=CVEOut)
def get_cve(cve_id: str, db: Session = Depends(get_db)):
    rec = db.query(CVERecord).filter(CVERecord.cve_id == cve_id.upper()).one_or_none()
    if not rec:
        raise HTTPException(status_code=404, detail="CVE not found")
    return CVEOut(**rec.to_dict())

@router.post("/ingest")
def ingest(payload: CVEIngestRequest, db: Session = Depends(get_db)):
    results = ingest_cves(db, [cid.upper() for cid in payload.cve_ids])
    return {"ingested": [r.cve_id for r in results], "count": len(results)}
