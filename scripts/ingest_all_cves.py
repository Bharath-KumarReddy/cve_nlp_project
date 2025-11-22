import requests
from app.database import SessionLocal
from app.services.ingest import ingest_cves

NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_all_cve_ids():
    """
    Fetch ALL CVE IDs from NVD API using pagination.
    """
    all_cves = []
    start_index = 0
    page_size = 2000
    total_results = 1

    while start_index < total_results:
        params = {
            "resultsPerPage": page_size,
            "startIndex": start_index
        }

        print(f"Fetching page starting at {start_index}...")
        resp = requests.get(NVD_URL, params=params)

        if not resp.ok:
            print("Failed:", resp.text)
            break

        js = resp.json()
        total_results = js.get("totalResults", 0)
        vulns = js.get("vulnerabilities", [])

        for v in vulns:
            cve_id = v.get("cve", {}).get("id")
            if cve_id:
                all_cves.append(cve_id)

        start_index += page_size

    return all_cves


def ingest_all():
    print("Fetching ALL CVE IDs from NVD...")
    cve_ids = fetch_all_cve_ids()

    print(f"Found {len(cve_ids)} CVEs. Now ingesting...")
    db = SessionLocal()

    try:
        ingest_cves(db, cve_ids)
        print("DONE: All CVEs ingested into database.")
    finally:
        db.close()


if __name__ == "__main__":
    ingest_all()
