# import streamlit as st
# import requests
# import os

# API_URL = os.getenv("API_URL", "http://localhost:8000")

# st.set_page_config(page_title="CVE NLP Database", layout="wide")
# st.title("CVE NLP Database")

# # Sidebar: Search and Ingest
# st.sidebar.header("Search CVEs")
# q = st.sidebar.text_input("Query", "")
# severity = st.sidebar.selectbox("Severity", ["", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
# year = st.sidebar.text_input("Year", "")
# limit = st.sidebar.slider("Limit", 1, 100, 10)
# offset = st.sidebar.number_input("Offset", min_value=0, value=0)

# if st.sidebar.button("Search"):
#     params = {"q": q, "severity": severity, "year": year, "limit": limit, "offset": offset}
#     params = {k: v for k, v in params.items() if v}
#     resp = requests.get(f"{API_URL}/cves", params=params)
#     if resp.ok:
#         cves = resp.json()
#         st.session_state["cves"] = cves
#     else:
#         st.error(f"Error: {resp.text}")

# # Show search results
# cves = st.session_state.get("cves", [])
# if cves:
#     st.subheader(f"Results ({len(cves)})")
#     for cve in cves:
#         with st.expander(f"{cve['cve_id']} - {cve.get('severity', '')}"):
#             st.write(cve)
# else:
#     st.info("No CVEs to display. Use the search form.")

# # Ingest new CVEs
# st.sidebar.header("Ingest CVEs")
# cve_ids = st.sidebar.text_area("CVE IDs (comma-separated)")
# if st.sidebar.button("Ingest"):
#     ids = [cid.strip() for cid in cve_ids.split(",") if cid.strip()]
#     if ids:
#         resp = requests.post(f"{API_URL}/cves/ingest", json={"cve_ids": ids})
#         if resp.ok:
#             st.sidebar.success(f"Ingested: {resp.json()['ingested']}")
#         else:
#             st.sidebar.error(f"Error: {resp.text}")
#     else:
#         st.sidebar.warning("Please enter at least one CVE ID.")

# # Visualizations
# st.header("Visualizations")
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("CVE Trends by Year")
#     resp = requests.get(f"{API_URL}/analysis/trends")
#     if resp.ok:
#         data = resp.json()
#         st.bar_chart(data["counts"])
#         if os.path.exists(data["chart"]):
#             st.image(data["chart"], caption="CVE Trends by Year")
#     else:
#         st.error("Failed to load trends.")

# with col2:
#     st.subheader("Severity Distribution")
#     resp = requests.get(f"{API_URL}/analysis/severity-distribution")
#     if resp.ok:
#         data = resp.json()
#         st.bar_chart(data["counts"])
#         if os.path.exists(data["chart"]):
#             st.image(data["chart"], caption="Severity Distribution")
#     else:
#         st.error("Failed to load severity distribution.")


import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="CVE NLP Database", layout="wide")
st.title("CVE NLP Database")

# Sidebar: Search and Ingest
st.sidebar.header("Search CVEs")
q = st.sidebar.text_input("Query", "")
severity = st.sidebar.selectbox("Severity", ["", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
year = st.sidebar.text_input("Year", "")
limit = st.sidebar.slider("Limit", 1, 100, 10)
offset = st.sidebar.number_input("Offset", min_value=0, value=0)

if st.sidebar.button("Search"):
    params = {"q": q, "severity": severity, "year": year, "limit": limit, "offset": offset}
    params = {k: v for k, v in params.items() if v}
    resp = requests.get(f"{API_URL}/cves", params=params)
    if resp.ok:
        cves = resp.json()
        st.session_state["cves"] = cves
    else:
        st.error(f"Error: {resp.text}")

# Show search results
cves = st.session_state.get("cves", [])

# Check if there is any data in the backend for visualizations
show_visualizations = False
try:
    resp = requests.get(f"{API_URL}/analysis/trends")
    if resp.ok and resp.json().get("counts"):
        show_visualizations = any(resp.json()["counts"].values())
except Exception:
    pass

if cves:
    st.subheader(f"Results ({len(cves)})")
    for cve in cves:
        with st.expander(f"{cve['cve_id']} - {cve.get('severity', '')}"):
            st.write(cve)
elif show_visualizations:
    st.info("No CVEs to display. Use the search form.")
else:
    st.info("Welcome! Use the search or ingest form to get started.")

# Ingest new CVEs
st.sidebar.header("Ingest CVEs")
cve_ids = st.sidebar.text_area("CVE IDs (comma-separated)")
if st.sidebar.button("Ingest"):
    ids = [cid.strip() for cid in cve_ids.split(",") if cid.strip()]
    if ids:
        resp = requests.post(f"{API_URL}/cves/ingest", json={"cve_ids": ids})
        if resp.ok:
            st.sidebar.success(f"Ingested: {resp.json()['ingested']}")
        else:
            st.sidebar.error(f"Error: {resp.text}")
    else:
        st.sidebar.warning("Please enter at least one CVE ID.")

# Only show visualizations if there is data
if show_visualizations:
    st.header("Visualizations")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("CVE Trends by Year")
        resp = requests.get(f"{API_URL}/analysis/trends")
        if resp.ok:
            data = resp.json()
            st.bar_chart(data["counts"])
        else:
            st.error("Failed to load trends.")

    with col2:
        st.subheader("Severity Distribution")
        resp = requests.get(f"{API_URL}/analysis/severity-distribution")
        if resp.ok:
            data = resp.json()
            st.bar_chart(data["counts"])
        else:
            st.error("Failed to load severity distribution.")
