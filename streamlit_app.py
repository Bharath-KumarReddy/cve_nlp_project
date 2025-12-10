import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="🛡️ CVE Intelligence Hub",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main .block-container {padding: 2rem; max-width: 100%;}
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem; border-radius: 15px; margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1); text-align: center;
    }
    .main-header h1 {color: white !important; font-size: 3rem; font-weight: 800; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);}
    .main-header p {color: rgba(255,255,255,0.95) !important; font-size: 1.2rem; margin-top: 0.5rem;}
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem; border-radius: 15px; text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); transition: transform 0.3s; height: 100%;
    }
    .feature-card:hover {transform: translateY(-10px); box-shadow: 0 8px 16px rgba(0,0,0,0.2);}
    .feature-card h3 {font-size: 3rem; margin-bottom: 1rem;}
    .stButton>button {
        width: 100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; padding: 0.75rem 1.5rem; font-weight: 600;
        border-radius: 10px; font-size: 1.1rem;
    }
    .stButton>button:hover {transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102,126,234,0.4);}
    div[data-testid="stMetricValue"] {font-size: 2rem; font-weight: 700;}
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"
if 'cves' not in st.session_state:
    st.session_state.cves = []

with st.sidebar:
    st.markdown("## 🎯 Navigation")
    page = st.radio("Navigation Menu", ["🏠 Home", "🔍 Search CVEs", "📊 Analytics", "📥 Ingest Data"], label_visibility="collapsed")
    st.session_state.page = page
    st.markdown("---")
    st.markdown("## 📈 Quick Stats")
    try:
        resp = requests.get(f"{API_URL}/cves", params={"limit": 1}, timeout=2)
        if resp.ok:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Error")
    except:
        st.warning("⚠️ API Offline")
    st.markdown("---")
    st.info("💡 **CVE Intelligence Hub**\\n\\nAdvanced vulnerability tracking powered by NLP")

if st.session_state.page == "🏠 Home":
    st.markdown("""<div class="main-header"><h1>🛡️ CVE Intelligence Hub</h1><p>Advanced Vulnerability Tracking & Analysis System</p></div>""", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class="feature-card"><h3>🔍</h3><h4>Smart Search</h4><p>Advanced CVE search with NLP filters</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="feature-card"><h3>📊</h3><h4>Analytics</h4><p>Visualize vulnerability trends</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="feature-card"><h3>📥</h3><h4>Data Ingestion</h4><p>Import from multiple sources</p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="feature-card"><h3>🎯</h3><h4>Tracking</h4><p>Monitor critical vulnerabilities</p></div>""", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🚀 Getting Started")
        st.markdown("""Welcome to **CVE Intelligence Hub**! This platform helps you:
- 🔎 **Search & Filter** vulnerabilities with advanced queries
- 📈 **Analyze Trends** to understand patterns over time
- 🎯 **Track Severity** and monitor critical issues
- 📊 **Visualize Data** with interactive charts

#### Quick Actions:
1. Navigate using the sidebar menu
2. Start by ingesting CVE data
3. Explore analytics to see trends
4. Use search to find specific vulnerabilities""")
    with col2:
        st.markdown("### 🎓 Resources")
        st.markdown("""**Severity Levels:**
- 🔴 CRITICAL: 9.0-10.0
- 🟠 HIGH: 7.0-8.9
- 🟡 MEDIUM: 4.0-6.9
- 🔵 LOW: 0.1-3.9

**Links:**
- [NVD Database](https://nvd.nist.gov/)
- [CVE.org](https://cve.org/)
- [MITRE](https://cve.mitre.org/)""")
    try:
        resp = requests.get(f"{API_URL}/analysis/trends", timeout=2)
        if resp.ok and resp.json().get("counts"):
            st.markdown("---")
            st.markdown("### 📊 Database Overview")
            col1, col2, col3, col4 = st.columns(4)
            trends = resp.json()["counts"]
            total = sum(trends.values())
            with col1:
                st.metric("Total CVEs", f"{total:,}")
            sev_resp = requests.get(f"{API_URL}/analysis/severity-distribution", timeout=2)
            if sev_resp.ok:
                sev = sev_resp.json()["counts"]
                with col2:
                    st.metric("Critical", sev.get("CRITICAL", 0))
                with col3:
                    st.metric("High", sev.get("HIGH", 0))
                with col4:
                    st.metric("Medium", sev.get("MEDIUM", 0))
    except:
        pass

elif st.session_state.page == "🔍 Search CVEs":
    st.markdown("""<div class="main-header"><h1>🔍 Search CVE Database</h1><p>Find and explore vulnerabilities</p></div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        query = st.text_input("🔎 Search Query", placeholder="Enter CVE ID or keywords...")
    with col2:
        severity = st.selectbox("⚠️ Severity", ["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    with col3:
        year = st.text_input("📅 Year", placeholder="e.g., 2024")
    col1, col2 = st.columns([1, 3])
    with col1:
        limit = st.slider("Results", 5, 50, 20)
    with col2:
        if st.button("🔍 Search CVEs"):
            with st.spinner("Searching..."):
                params = {"q": query, "severity": severity if severity != "All" else "", "year": year, "limit": limit}
                params = {k: v for k, v in params.items() if v}
                try:
                    resp = requests.get(f"{API_URL}/cves", params=params, timeout=10)
                    if resp.ok:
                        st.session_state.cves = resp.json()
                        st.success(f"✅ Found {len(st.session_state.cves)} results!")
                    else:
                        st.error(f"❌ Error: {resp.text}")
                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")
    if st.session_state.cves:
        st.markdown(f"### 📋 Results: {len(st.session_state.cves)} CVEs")
        for cve in st.session_state.cves:
            with st.expander(f"🔒 {cve['cve_id']} - {cve.get('severity', 'N/A')}", expanded=False):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**CVE ID:** `{cve['cve_id']}`")
                    st.markdown(f"**Description:** {cve.get('description', 'N/A')[:300]}...")
                    st.markdown(f"**Published:** {cve.get('published_date', 'N/A')}")
                with col2:
                    st.markdown(f"**Severity:** `{cve.get('severity', 'N/A')}`")
                    st.markdown(f"**CVSS:** `{cve.get('cvss_score', 'N/A')}`")
                    st.markdown(f"**Vector:** `{cve.get('attack_vector', 'N/A')}`")
    else:
        st.info("💡 No results. Use the search form above.")

elif st.session_state.page == "📊 Analytics":
    st.markdown("""<div class="main-header"><h1>📊 Analytics Dashboard</h1><p>Visualize vulnerability trends and patterns</p></div>""", unsafe_allow_html=True)
    try:
        resp = requests.get(f"{API_URL}/analysis/trends", timeout=5)
        if resp.ok and resp.json().get("counts"):
            tab1, tab2 = st.tabs(["📈 Trends", "⚠️ Severity"])
            with tab1:
                st.markdown("### 📈 CVE Trends Over Time")
                data = resp.json()["counts"]
                df = pd.DataFrame(list(data.items()), columns=["Year", "Count"])
                col1, col2 = st.columns([3, 1])
                with col1:
                    fig = px.line(df, x="Year", y="Count", markers=True, title="CVE Count by Year")
                    fig.update_traces(line_color='#667eea', line_width=3)
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.metric("Total CVEs", f"{df['Count'].sum():,}")
                    st.metric("Average/Year", f"{df['Count'].mean():.0f}")
                    st.metric("Peak Year", df.loc[df['Count'].idxmax(), 'Year'])
            with tab2:
                st.markdown("### ⚠️ Severity Distribution")
                sev_resp = requests.get(f"{API_URL}/analysis/severity-distribution", timeout=5)
                if sev_resp.ok:
                    sev_data = sev_resp.json()["counts"]
                    df_sev = pd.DataFrame(list(sev_data.items()), columns=["Severity", "Count"])
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        colors = {"CRITICAL": "#e74c3c", "HIGH": "#f39c12", "MEDIUM": "#f1c40f", "LOW": "#3498db"}
                        fig = go.Figure(data=[go.Pie(labels=df_sev["Severity"], values=df_sev["Count"], marker=dict(colors=[colors.get(s, "#95a5a6") for s in df_sev["Severity"]]), hole=0.4)])
                        fig.update_layout(title="Severity Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                    with col2:
                        for _, row in df_sev.iterrows():
                            st.metric(row["Severity"], f"{row['Count']:,}")
        else:
            st.warning("📊 No data available. Please ingest some CVEs first!")
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")

elif st.session_state.page == "📥 Ingest Data":
    st.markdown("""<div class="main-header"><h1>📥 Data Ingestion Center</h1><p>Import CVE data into your database</p></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 📝 Enter CVE IDs")
        cve_ids = st.text_area("CVE IDs (one per line or comma-separated)", placeholder="CVE-2024-1234\\nCVE-2024-5678", height=200)
    with col2:
        st.markdown("### 💡 Examples")
        st.code("CVE-2024-1234", language="text")
        st.code("CVE-2023-5678", language="text")
        st.code("CVE-2022-9012", language="text")
    if st.button("📥 Ingest CVEs"):
        ids = [cid.strip() for cid in cve_ids.replace(",", "\\n").split("\\n") if cid.strip()]
        if ids:
            with st.spinner(f"🔄 Ingesting {len(ids)} CVEs..."):
                try:
                    resp = requests.post(f"{API_URL}/cves/ingest", json={"cve_ids": ids}, timeout=30)
                    if resp.ok:
                        result = resp.json()
                        st.success(f"✅ Successfully ingested {result['ingested']} CVEs!")
                        if result.get('failed'):
                            st.warning(f"⚠️ Failed: {', '.join(result['failed'])}")
                    else:
                        st.error(f"❌ Error: {resp.text}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter at least one CVE ID.")

st.markdown("---")
st.markdown("""<div style="text-align: center; color: #7f8c8d; padding: 2rem;"><p>🛡️ CVE Intelligence Hub | Built with Streamlit & FastAPI | © 2025</p></div>""", unsafe_allow_html=True)
