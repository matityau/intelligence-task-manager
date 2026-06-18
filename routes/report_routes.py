from fastapi import APIRouter,HTTPException
from database.mission_db import missions_table
from database.agent_db import agent_table

router = APIRouter()

@router.get("/summary")
def general_system_report():
    try:
        active_agents = agent_table.count_active_agents()
        total_mission = missions_table.count_all_missions()
        


