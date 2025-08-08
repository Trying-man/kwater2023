from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String, unique=True, nullable=False)
    published_at = Column(DateTime, nullable=False)
    sentiment = Column(String(10))  # Positive, Neutral, Negative
    created_at = Column(DateTime, default=func.now()) 