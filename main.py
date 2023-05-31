import os
import sqlalchemy
import databases
from sqlalchemy.orm import sessionmaker


from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import psycopg2


# print("Loookkkkk heeerreeeeee ")
print("------> " + os.environ['DATABASE_URL'])

app = FastAPI()


# engine = sqlalchemy.create_engine(os.environ['DATABASE_URL']) 

engine = sqlalchemy.create_engine("postgresql://postgres:t3chl@b2023@localhost:5432/sur_gui_db") 



# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# database = databases.Database(engine)

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/ben")
def index():
    return {"title": "Advising"}

connection = psycopg2.connect(
    host="192.168.169.107",
    database="sur_gui_db",
    user="postgres",
    password="t3chl@b2023"
)

print("connnection successful")

cur = connection.cursor()

##cur.execute("CREATE TABLE soccer_players (id SERIAL PRIMARY KEY, name VARCHAR(255), age INTEGER)")
cur.execute("INSERT INTO soccer_players (id,name, age) VALUES(%s,%s, %s)", (2323,"Miguel", 20))

connection.commit()




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

connection.close()