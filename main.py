from fastapi import FastAPI
import uvicorn
from database.db_connection import create_database_and_tables as start


app = FastAPI() 

start.create_database()
start.create_tables()


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)