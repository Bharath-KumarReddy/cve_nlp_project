from app.database import SessionLocal
from app.services.ingest import ingest_cves

# Popular sample CVEs
SAMPLE_IDS = [
    "CVE-2021-44228",  # Log4Shell
    "CVE-2023-4863",   # libwebp
    "CVE-2017-0144"    # EternalBlue
]

if __name__ == "__main__":
    db = SessionLocal()
    try:
        ingest_cves(db, SAMPLE_IDS)
        print("Sample CVEs ingested.")
    finally:
        db.close()
