from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

DATABASE_URl = os.environ.get("DB_CONN")

engine = create_engine(DATABASE_URl)

sessionLocal = sessionmaker(autoflush=False, bind=engine, autocommit=False)

Base = declarative_base()


def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()
