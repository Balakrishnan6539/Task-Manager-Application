from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
env_file = BASE_DIR / ".env"

load_dotenv(env_file)

db_url = os.getenv("DB_URL") 
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()