from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import databases
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
raw_password = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")

encoded_password = quote_plus(raw_password)
DATABASE_URL = f"postgresql://{DATABASE_USER}:{encoded_password}@{DATABASE_HOST}:5432/{DATABASE_NAME}"

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
