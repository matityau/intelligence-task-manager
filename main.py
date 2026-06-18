from fastapi import FastAPI
import uvicorn
from database.db_connection import create_database_and_tables as start
from routes import mission_routes,agent_routes,report_routes
import os
import logging

os.makedirs("logs", exist_ok=True)

logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(message)s",
                    handlers=[logging.FileHandler("logs/app.log"),logging.StreamHandler()]
)


logger = logging.getLogger(__name__)

app = FastAPI() 
logger.info("Application start upload")

start.create_database()
start.create_tables()

app.include_router(agent_routes.router,prefix="/agents",tags=["Agents"])
app.include_router(mission_routes.router,prefix="/missions",tags=["Missions"])
app.include_router(report_routes.router,prefix="/agents",tags=["Reports"])


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)