from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.analysis import trends_by_year, severity_distribution

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/trends")
def trends(db: Session = Depends(get_db)):
    return trends_by_year(db)

@router.get("/severity-distribution")
def severity_dist(db: Session = Depends(get_db)):
    return severity_distribution(db)
