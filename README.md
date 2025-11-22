# CVE NLP Database

End-to-end pipeline to collect CVEs (API + scrape), extract key info via NLP (spaCy + Transformers),
store in SQLite (SQLAlchemy), and expose a FastAPI for querying and analysis.

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