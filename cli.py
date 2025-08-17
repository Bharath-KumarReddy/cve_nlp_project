import json
import typer
from typing import List, Optional

from app.services.ingest import ingest_cves
from app.services.search import search_cves
from app.database import SessionLocal

app = typer.Typer(add_completion=False)

@app.command()
def ingest(ids: List[str] = typer.Option(..., "--ids", help="CVE IDs")):
    db = SessionLocal()
    try:
        results = ingest_cves(db, ids)
        typer.echo(f"Ingested/updated {len(results)} CVEs.")
    finally:
        db.close()

@app.command()
def search(q: str, severity: Optional[str] = None, limit: int = 10, offset: int = 0):
    db = SessionLocal()
    try:
        rows, total = search_cves(db, q=q, severity=severity, limit=limit, offset=offset)
        typer.echo(json.dumps({
            "total": total,
            "results": [r.to_dict() for r in rows]
        }, indent=2))
    finally:
        db.close()

if __name__ == "__main__":
    app()
