from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.collectors.nvd_api import fetch_cve, parse_nvd_cve
from app.collectors.cve_org_scraper import scrape_cve_org
from app.extractors.extractor import enrich_record
from app.models import CVERecord

def _parse_dt(dt_str: str | None):
    if not dt_str:
        return None
    try:
        # NVD uses ISO8601 strings, e.g. "2021-12-10T00:00:00.000"
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except Exception:
        try:
            return datetime.fromisoformat(dt_str)
        except Exception:
            return None

def upsert_record(db: Session, data: Dict[str, Any], raw: Dict[str, Any], source: str) -> CVERecord:
    cve_id = data.get("cve_id")
    rec = db.query(CVERecord).filter(CVERecord.cve_id == cve_id).one_or_none()
    if not rec:
        rec = CVERecord(cve_id=cve_id)
        db.add(rec)

    rec.source = source
    rec.description = data.get("description")
    rec.published = _parse_dt(data.get("published"))
    rec.last_modified = _parse_dt(data.get("last_modified"))
    rec.cwes = data.get("cwes") or []
    rec.vendors = data.get("vendors") or []
    rec.products = data.get("products") or []
    rec.cvss_score = data.get("cvss_score")
    rec.cvss_vector = data.get("cvss_vector")
    rec.severity = data.get("severity")
    rec.raw = raw
    rec.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(rec)
    return rec

def ingest_cves(db: Session, cve_ids: List[str]) -> List[CVERecord]:
    out = []
    for cid in cve_ids:
        cid = cid.strip().upper()
        # Prefer NVD (structured), fallback to cve.org scraper
        nvd = fetch_cve(cid)
        if nvd:
            parsed = parse_nvd_cve(nvd)
            parsed = enrich_record(parsed)
            rec = upsert_record(db, parsed, raw={"nvd": nvd}, source="nvd")
            # after NLP, update NLP results
            rec.entities = parsed.get("entities")
            rec.facts = parsed.get("facts")
            db.commit()
            db.refresh(rec)
            out.append(rec)
            continue

        scraped = scrape_cve_org(cid)
        if scraped:
            scraped = enrich_record(scraped)
            rec = upsert_record(db, scraped, raw={"cve_org": scraped}, source="cve.org")
            rec.entities = scraped.get("entities")
            rec.facts = scraped.get("facts")
            db.commit()
            db.refresh(rec)
            out.append(rec)
        else:
            # Create an empty placeholder if nothing found (optional)
            pass
    return out
