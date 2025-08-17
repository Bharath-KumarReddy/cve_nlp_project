from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models import CVERecord

def search_cves(db: Session, q: Optional[str] = None, severity: Optional[str] = None,
                year: Optional[int] = None, limit: int = 10, offset: int = 0) -> Tuple[List[CVERecord], int]:
    query = db.query(CVERecord)
    if q:
        like = f"%{q}%"
        query = query.filter(or_(CVERecord.cve_id.ilike(like), CVERecord.description.ilike(like)))
    if severity:
        query = query.filter(CVERecord.severity == severity.upper())
    if year:
        query = query.filter(func.strftime("%Y", CVERecord.published) == str(year))
    total = query.count()
    rows = query.order_by(CVERecord.published.desc().nullslast(), CVERecord.cve_id.desc()) \
                .offset(offset).limit(limit).all()
    return rows, total
