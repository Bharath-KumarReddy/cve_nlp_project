import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# SQLite by default; can be overridden (e.g., "postgresql+psycopg2://user:pass@host/dbname")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/db/cve.db")

# Optional NVD API key to improve rate limits (from https://nvd.nist.gov/developers/request-an-api-key)
NVD_API_KEY = os.getenv("NVD_API_KEY")