from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "database/plants_database.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

""" -----------------------------------------------------------------------------------------------
 Creates a lightweight sqlite database, fancy with sqlalchemy
----------------------------------------------------------------------------------------------- """
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

""" -----------------------------------------------------------------------------------------------
 For dependency injection
----------------------------------------------------------------------------------------------- """
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
