from fastapi import APIRouter,HTTPException
from database.mission_db import missions_table
from database.agent_db import agent_table
import logging


router = APIRouter()

logger = logging.getLogger(__name__)
logging.getLogger("mysql.connector").setLevel(logging.WARNING)

@router.get("/summary")
def general_system_report():
    try:
        logger.info("GET/ reports caleled/summary")
        active_agents = agent_table.count_active_agents()
        if not active_agents:
            active_agents = []
        total_mission = missions_table.count_all_missions()
        if not total_mission:
            total_mission = []
        open_mission = missions_table.count_open_missions()
        if not open_mission:
            open_mission = []
        compleeted = missions_table.count_by_status("COMPLETED")
        if not compleeted:
            compleeted = []
        failed = missions_table.count_by_status("FAILED")
        if not failed:
            failed = []
        canceled = missions_table.count_by_status("CANCELLED")
        if not canceled:
            canceled = []

        return {
            "active_agents_count": active_agents,
            "total_missions": total_mission,
            "open_missions": open_mission,
            "completed_missions": compleeted,
            "failed_missions":failed,
            "canceled":canceled
            }
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error{e}")
    
@router.get("/missions-by-status")
def get_missions_by_status():
    try:
        logger.info("GET/ reports/missions-by-status caleled")
        new = missions_table.count_by_status('New')
        assigned =missions_table.count_by_status('ASSIGNED')
        in_p =missions_table.count_by_status('IN_PROGRESS')
        completed =missions_table.count_by_status('COMPLETED')
        failed =missions_table.count_by_status('FAILED')
        canceled =missions_table.count_by_status('CANCELLED')
        return {
            "new": new,
            "assigned": assigned,
            "in_progress": in_p,
            "completed": completed,
            "failed":failed,
            "canceled":canceled
            }
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error{e}")
    
@router.get("/top-agent")
def top_agent():
    try:
        logger.info("GET/ reports/summary caleled")
        top = missions_table.get_top_agent()
        logger.info("GET/ reports/summary caleled")
        return top
    except Exception as e :
        raise HTTPException(status_code=500,detail= f"error: {e}")
    