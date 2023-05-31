# main.py
from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from databases import Database
from urllib.parse import quote_plus
import os

DATABASE_USER = quote_plus("")
DATABASE_URL = "postgresql://postgres:" + DATABASE_USER + "@/"

database = Database(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("email", String(50)),
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


@app.post("/users/")
async def create_user(user: dict):
    query = users.insert().values(name=user['name'], email=user['email'])
    last_record_id = await database.execute(query)
    return {**user, "id": last_record_id}
