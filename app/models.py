from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(100))
    specialty = Column(String(100))
    hospital = Column(String(100))
    notes = Column(Text)
    summary = Column(Text)
    follow_up_date = Column(String(50))
    sentiment = Column(String(50))
    opportunity_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)