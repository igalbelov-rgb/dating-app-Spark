from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from pydantic_settings import BaseSettings # שימוש בחבילה המעודכנת
import os

class Settings(BaseSettings):
    # עדיף להשתמש ב-os.getenv כדי שזה יעבוד גם ב-Docker וגם מקומית
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/dating_app")

    class Config:
        env_file = ".env"

settings = Settings()

# pool_pre_ping מוודא שהחיבור לא "מת" בתוך הקונטיינר
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SurveyResult(Base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    # הוספת nullable=False לשדות חובה לפי דרישות ה-Review
    profession = Column(String, nullable=False)
    bio = Column(String, nullable=False)
    sentiment_score = Column(Float)
    sentiment_label = Column(String)

def init_db() -> None:
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()