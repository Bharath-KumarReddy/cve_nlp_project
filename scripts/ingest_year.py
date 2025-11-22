import requests
from app.database import SessionLocal
from app.services.ingest import ingest_cves

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_cve_ids_by_year(year: int):
    """
    Fetch all CVE IDs for a given year using NVD API pagination.
    """
    cve_ids = []
    start = 0
    total = 1  # unknown initially
    page_size = 2000

    print(f"Fetching CVEs for {year}...")

    while start < total:
        params = {
            "pubStartDate": f"{year}-01-01T00:00:00.000",
            "pubEndDate": f"{year}-12-31T23:59:59.000",
            "resultsPerPage": page_size,
            "startIndex": start
        }

        resp = requests.get(NVD_URL, params=params)
        if not resp.ok:
            print("❌ Failed to fetch page:", resp.text)
            break

        data = resp.json()
        total = data.get("totalResults", 0)
        vulnerabilities = data.get("vulnerabilities", [])

        for v in vulnerabilities:
            cve = v.get("cve", {})
            cve_id = cve.get("id")
            if cve_id:
                cve_ids.append(cve_id)

        print(f"✔ Fetched {len(cve_ids)} so far...")

        start += page_size

    print(f"Total CVEs fetched for year {year}: {len(cve_ids)}")
    return cve_ids


def ingest_year(year: int):
    ids = fetch_cve_ids_by_year(year)

    print(f"🚀 Ingesting {len(ids)} CVEs into the database...")

    db = SessionLocal()
    try:
        ingest_cves(db, ids)
        print("✅ DONE: Year ingested successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    for year in range(2002, 2025):
        ingest_year(year)
