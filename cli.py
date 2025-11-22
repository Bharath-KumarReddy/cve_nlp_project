import json
import typer
import requests
from typing import List, Optional

from app.services.ingest import ingest_cves
from app.services.search import search_cves
from app.database import SessionLocal

app = typer.Typer(add_completion=False)

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def fetch_all_cve_ids() -> List[str]:
    """
    Fetch ALL CVE IDs from NVD using pagination.
    """
    all_ids = []
    start = 0
    total = 1  # unknown until first request
    page_size = 2000

    typer.echo("🚀 Fetching ALL CVE IDs from NVD...")

    while start < total:
        params = {
            "resultsPerPage": page_size,
            "startIndex": start
        }
        typer.echo(f"Fetching page starting at index {start} ...")

        resp = requests.get(NVD_URL, params=params)

        if not resp.ok:
            typer.echo(f"❌ Failed to fetch: {resp.text}")
            break

        data = resp.json()
        total = data.get("totalResults", 0)
        vulns = data.get("vulnerabilities", [])

        for v in vulns:
            cve_id = v.get("cve", {}).get("id")
            if cve_id:
                all_ids.append(cve_id)

        start += page_size

    typer.echo(f"✔ Total CVEs found: {len(all_ids)}")
    return all_ids


@app.command()
def ingest(ids: List[str] = typer.Option(..., "--ids", help="CVE IDs")):
    """
    Ingest specific CVE IDs.
    """
    db = SessionLocal()
    try:
        results = ingest_cves(db, ids)
        typer.echo(f"Ingested/updated {len(results)} CVEs.")
    finally:
        db.close()


@app.command()
def ingest_all():
    """
    Ingest ALL CVEs available in the NVD database.
    WARNING: This may take a very long time.
    """
    ids = fetch_all_cve_ids()

    if len(ids) == 0:
        typer.echo("❌ No CVEs found.")
        raise typer.Exit()

    db = SessionLocal()
    try:
        typer.echo("🚀 Starting ingestion into database...")
        results = ingest_cves(db, ids)
        typer.echo(f"✔ DONE. Ingested {len(results)} CVEs.")
    finally:
        db.close()


@app.command()
def search(q: str, severity: Optional[str] = None, limit: int = 10, offset: int = 0):
    """
    Search CVEs in the local SQLite database.
    """
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