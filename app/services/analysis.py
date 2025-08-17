from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import CVERecord
import os
import pandas as pd
import matplotlib.pyplot as plt

def trends_by_year(db: Session) -> Dict[str, Any]:
    rows = db.query(func.strftime("%Y", CVERecord.published), func.count(CVERecord.id)) \
             .group_by(func.strftime("%Y", CVERecord.published)).all()
    data = {year or "Unknown": count for year, count in rows}
    # chart
    os.makedirs("data/reports", exist_ok=True)
    if data:
        df = pd.DataFrame({"year": list(data.keys()), "count": list(data.values())}).sort_values("year")
        plt.figure()
        plt.plot(df["year"], df["count"])
        plt.title("CVE Count by Year")
        plt.xlabel("Year")
        plt.ylabel("Count")
        plt.tight_layout()
        path = "data/reports/cve_trends_by_year.png"
        plt.savefig(path)
    return {"counts": data, "chart": "data/reports/cve_trends_by_year.png"}

def severity_distribution(db: Session) -> Dict[str, Any]:
    rows = db.query(CVERecord.severity, func.count(CVERecord.id)) \
             .group_by(CVERecord.severity).all()
    data = {sev or "UNKNOWN": count for sev, count in rows}
    # chart
    os.makedirs("data/reports", exist_ok=True)
    if data:
        df = pd.DataFrame({"severity": list(data.keys()), "count": list(data.values())})
        plt.figure()
        plt.bar(df["severity"], df["count"])
        plt.title("Severity Distribution")
        plt.xlabel("Severity")
        plt.ylabel("Count")
        plt.tight_layout()
        path = "data/reports/severity_distribution.png"
        plt.savefig(path)
    return {"counts": data, "chart": "data/reports/severity_distribution.png"}
