# CVE NLP Database

End-to-end pipeline to collect CVEs (API + scrape), extract key info via NLP (spaCy + Transformers),
store in SQLite (SQLAlchemy), and expose a FastAPI for querying and analysis.


# CVE Database Automation Using NLP and FastAPI

An AI-powered platform that automates the ingestion, enrichment, storage, search, and visualization of CVE (Common Vulnerabilities and Exposures) data using **Natural Language Processing (NLP)** and **FastAPI**.

---

## 📌 Project Overview

Cybersecurity vulnerabilities are published as CVEs every year in large volumes. Important information such as attack method, impact, affected components, and severity is usually embedded in unstructured text. Manually analyzing these CVEs is time-consuming and inefficient.

This project builds an **automated CVE intelligence system** that fetches CVE data, processes it using NLP techniques, stores structured information, and provides APIs and a web-based dashboard for easy access and visualization.

---

## 🚀 Features

- Automatic CVE ingestion from official sources
- NLP-based information extraction
- Zero-shot classification and severity inference
- Structured SQLite database storage
- FastAPI-powered REST APIs
- Interactive Streamlit dashboard
- Command-line interface for automation
- Bulk CVE ingestion by year

---

## 🧠 NLP Techniques Used

### Named Entity Recognition (NER)
Extracts:
- Vendors
- Software products
- Attack types
- System components

### Subject–Verb–Object (SVO) Extraction
Identifies core vulnerability actions:
- Who performed the action
- What action was performed
- What was targeted

### Zero-Shot Classification
Automatically predicts:
- Impact category (RCE, DoS, Privilege Escalation)
- Attack vector (Network, Local, Adjacent)
- Component type (OS, Library, Browser)

### Severity Normalization
Infers severity from CVSS score when missing.

---

## 🏗️ System Architecture

### Workflow

1. User inputs CVE IDs (API / CLI / UI)
2. Data fetched from NVD API and CVE.org
3. Raw data normalized and cleaned
4. NLP pipeline enriches CVE descriptions
5. Data stored in SQLite database
6. FastAPI exposes REST endpoints
7. Streamlit UI visualizes results

---

## 📁 Project Structure

```
cve_nlp_project/
│
├── app/
│   ├── api/
│   │   ├── routers/
│   │   │   ├── cves.py
│   │   │   └── analysis.py
│   │   └── main.py
│   │
│   ├── collectors/
│   │   ├── nvd_api.py
│   │   └── cve_org_scraper.py
│   │
│   ├── services/
│   │   ├── ingest.py
│   │   ├── search.py
│   │   └── analysis.py
│   │
│   ├── nlp/
│   │   ├── preprocess.py
│   │   ├── ner.py
│   │   ├── classify.py
│   │   └── parse.py
│   │
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── streamlit_app.py
├── cli.py
├── scripts/
│   └── ingest_year.py
│
├── config.py
└── cves.db
```

---

## ⚙️ Setup Instructions

### Install Dependencies

```bash
pip install -r requirements.txt
```

### NVD API Configuration

Get your API key from:

```
https://nvd.nist.gov/developers/request-an-api-key
```

Update `config.py`:

```python
NVD_API_KEY = "your_api_key_here"
DATABASE_URL = "sqlite:///./cves.db"
```

---

## ▶️ Running the Project

### Start FastAPI Backend

```bash
uvicorn app.api.main:app --reload
```

### Start Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

---

## 🧪 CLI Commands

### Ingest Specific CVEs

```bash
python cli.py ingest --ids CVE-2021-44228 CVE-2023-4863
```

### Ingest All CVEs

```bash
python cli.py ingest-all
```

### Search CVEs

```bash
python cli.py search "apache"
```

### Bulk Ingest by Year

```bash
python scripts/ingest_year.py
```

---

## 🌐 API Endpoints

### Ingest CVEs

```
POST /cves/ingest
```

### Search CVEs

```
GET /cves?q=<query>&severity=<level>&year=<year>&limit=<n>&offset=<n>
```

### Get CVE Details

```
GET /cves/{cve_id}
```

### CVE Trends

```
GET /analysis/trends
```

### Severity Distribution

```
GET /analysis/severity-distribution
```

### Health Check

```
GET /health
```

---

## 📊 Streamlit Dashboard Features

- CVE search and filtering
- NLP enriched CVE details
- Year-wise vulnerability trends
- Severity distribution charts
- Interactive analytics dashboard

---

## 🛠️ Technologies Used

- Python
- FastAPI
- spaCy
- HuggingFace Transformers
- SQLite
- Streamlit
- SQLAlchemy
- BeautifulSoup

---

## ✅ Project Outcomes

- Automated CVE processing pipeline
- AI-powered vulnerability analysis
- Searchable structured CVE database
- Real-time visualization dashboard
- API-ready backend for integrations


## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

cp .env.example .env
python scripts/init_db.py
python scripts/ingest_sample.py

uvicorn app.api.main:app --reload --port 8000
# open: http://127.0.0.1:8000/docs
