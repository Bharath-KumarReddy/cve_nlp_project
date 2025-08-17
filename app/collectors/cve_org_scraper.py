import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any

# Fallback scraper for cve.org if NVD misses something
CVE_ORG_URL = "https://www.cve.org/CVERecord?id={cve_id}"

def scrape_cve_org(cve_id: str) -> Optional[Dict[str, Any]]:
    url = CVE_ORG_URL.format(cve_id=cve_id)
    r = requests.get(url, timeout=30)
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.text, "lxml")

    # The cve.org page layout may change; we try conservative selectors
    # Description
    desc = None
    h2 = soup.find(lambda tag: tag.name in ("h2", "h3") and "Description" in tag.text)
    if h2:
        # Next sibling paragraph
        p = h2.find_next("p")
        if p:
            desc = p.get_text(strip=True)

    # Published/Modified (best effort)
    def find_kv(label: str) -> Optional[str]:
        el = soup.find(lambda tag: tag.name in ("div", "span", "p", "li") and label in tag.text)
        if not el:
            return None
        txt = el.get_text(" ", strip=True)
        # e.g., "Published: 2021-12-10" -> after colon
        parts = txt.split(":")
        return parts[1].strip() if len(parts) > 1 else None

    published = find_kv("Published")
    modified = find_kv("Last Modified")

    return {
        "cve_id": cve_id,
        "description": desc,
        "published": published,
        "last_modified": modified,
        "cwes": [],
        "vendors": [],
        "products": [],
        "cvss_score": None,
        "cvss_vector": None,
        "severity": None
    }
