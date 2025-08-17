import os
import requests
from typing import Optional, Dict, Any
from config import NVD_API_KEY

NVD_ENDPOINT = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_cve(cve_id: str) -> Optional[Dict[str, Any]]:
    headers = {}
    if NVD_API_KEY:
        headers["apiKey"] = NVD_API_KEY
    params = {"cveId": cve_id}
    r = requests.get(NVD_ENDPOINT, params=params, headers=headers, timeout=30)
    if r.status_code != 200:
        return None
    js = r.json()
    vulns = js.get("vulnerabilities") or []
    if not vulns:
        return None
    return vulns[0].get("cve")

def parse_nvd_cve(nvd_cve: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize NVD schema -> our internal structure
    """
    id_ = nvd_cve.get("id")
    descriptions = nvd_cve.get("descriptions") or []
    desc_en = next((d.get("value") for d in descriptions if d.get("lang") == "en"), None) or \
              (descriptions[0]["value"] if descriptions else None)

    published = nvd_cve.get("published")
    last_modified = nvd_cve.get("lastModified")

    # CWE list
    weaknesses = nvd_cve.get("weaknesses") or []
    cwes = []
    for w in weaknesses:
        for d in w.get("description", []):
            if d.get("lang") == "en" and d.get("value"):
                cwes.append(d["value"])
    cwes = list(sorted(set(cwes)))

    # Vendors/products from configurations (if available)
    vendors, products = set(), set()
    configs = nvd_cve.get("configurations") or []
    for c in configs:
        for node in c.get("nodes", []):
            for m in node.get("cpeMatch", []):
                cpe = m.get("criteria") or ""
                parts = cpe.split(":")
                # cpe:2.3:a:apache:log4j:2.14.1:...
                if len(parts) >= 5:
                    vendor = parts[3]
                    product = parts[4]
                    if vendor and vendor != "*":
                        vendors.add(vendor)
                    if product and product != "*":
                        products.add(product)

    # CVSS
    score = None
    vector = None
    severity = None
    metrics = nvd_cve.get("metrics") or {}
    for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        arr = metrics.get(key) or []
        if arr:
            data = arr[0]
            cvssData = data.get("cvssData") or {}
            score = cvssData.get("baseScore")
            vector = cvssData.get("vectorString")
            severity = data.get("baseSeverity") or data.get("severity")
            break

    return {
        "cve_id": id_,
        "description": desc_en,
        "published": published,
        "last_modified": last_modified,
        "cwes": cwes,
        "vendors": sorted(vendors),
        "products": sorted(products),
        "cvss_score": score,
        "cvss_vector": vector,
        "severity": severity
    }
