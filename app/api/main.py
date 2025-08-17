from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.api.routers import cves as cves_router
from app.api.routers import analysis as analysis_router

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="CVE NLP Database", version="1.0.0")

@app.get("/health")
def health(db: Session = Depends(get_db)):
    return {"status": "ok"}

app.include_router(cves_router.router, prefix="/cves", tags=["CVE"])
app.include_router(analysis_router.router, prefix="/analysis", tags=["Analysis"])
