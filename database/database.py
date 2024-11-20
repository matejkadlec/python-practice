from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# Create base class for SQLAlchemy ORM models
Base = declarative_base()

# Create database engine
engine = create_engine(DATABASE_URL)

# Create session factory to generate sessions
SessionLocal = sessionmaker(autocommit=False, bind=engine)

def get_session() -> Session:
    # Return new session
    return SessionLocal()
