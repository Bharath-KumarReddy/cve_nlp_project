import os
from app.database import engine
from app.models import Base

os.makedirs("./data/db", exist_ok=True)
Base.metadata.create_all(bind=engine)
print("Database initialized at ./data/db/cve.db")