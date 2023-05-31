# main.py
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from databases import Database
from urllib.parse import quote_plus
import os

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
raw_password = os.getenv("DATABASE_PASSWORD")
DATABASE_PASSWORD = quote_plus(raw_password)
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
print("Database user", DATABASE_USER)
print("Database password", DATABASE_PASSWORD)
print("Database host", DATABASE_HOST)
print("Database name", DATABASE_NAME)
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/{DATABASE_NAME}"
database = Database(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("email", String(50)),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("description", String(200)),
    Column("price", Float),
)


engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    try:
        await database.connect()
        print("Successfully connected to the database")
    except Exception as e:
        print("An error occurred during connection: ", e)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}
