from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime
from .database import Base

class CVERecord(Base):
    __tablename__ = "cve_records"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String(32), unique=True, index=True, nullable=False)
    source = Column(String(32), default="nvd")
    description = Column(Text)
    published = Column(DateTime, nullable=True)
    last_modified = Column(DateTime, nullable=True)

    severity = Column(String(16), nullable=True)   # e.g., CRITICAL/HIGH/MEDIUM/LOW
    cvss_score = Column(Float, nullable=True)
    cvss_vector = Column(String(128), nullable=True)

    cwes = Column(JSON, nullable=True)        # list of strings
    vendors = Column(JSON, nullable=True)     # list of strings
    products = Column(JSON, nullable=True)    # list of strings

    entities = Column(JSON, nullable=True)    # [{text, label, source, char_span}]
    facts = Column(JSON, nullable=True)       # extracted triples, zero-shot labels
    raw = Column(JSON, nullable=True)         # raw source payload (for trace/debug)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "cve_id": self.cve_id,
            "source": self.source,
            "description": self.description,
            "published": self.published.isoformat() if self.published else None,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
            "severity": self.severity,
            "cvss_score": self.cvss_score,
            "cvss_vector": self.cvss_vector,
            "cwes": self.cwes or [],
            "vendors": self.vendors or [],
            "products": self.products or [],
            "entities": self.entities or [],
            "facts": self.facts or {},
        }
