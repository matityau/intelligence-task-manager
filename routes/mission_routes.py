from database.mission_db import missions_table
from fastapi import APIRouter,HTTPException,Query
from pydantic import BaseModel
from typing import Optional,Literal
from database.agent_db import agent_table
import logging
logger = logging.getLogger(__name__)
logging.getLogger("mysql.connector").setLevel(logging.WARNING)

router = APIRouter()


@router.get("")
def get_all_missins():
    all = missions_table.get_all_missions()
    if not all:
        return []
    return all

@router.get("/{id}")
def get_mission_by_id(id:int):
    try:
        mission = missions_table.get_mission_by_id(id)
        if not mission:
            raise HTTPException(status_code=404,detail=f"id  mission: {id} not found")
        return mission
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error: {e}")

class Mission(BaseModel):
    title:str
    description:str
    location:str
    difficulty:int
    importance:int
    

def calculate_risk_level(risc):
        if 2 <= risc <= 9:
            return "LOW"
        elif 10 <= risc <= 17:
             return "MEDIUM"
        elif 18 <= risc <= 24:
            return "HIGH"
        elif  risc >= 25:
            return "CRITICAL"

@router.post("",status_code=201)
def create_mission(data:Mission):

    try:
        if not data:
            raise HTTPException(status_code=400,detail=f"DATA not filed")
        
        if not 1<= data.difficulty <= 10:
             raise HTTPException(status_code=400,detail=f"difficulty must be between 1-10")
        
        if not 1<= data.importance <= 10:
             raise HTTPException(status_code=400,detail=f"importance must be between 1-10")
        data_dict = data.model_dump()
        
        mission = missions_table.create_mission(data_dict)
        if not mission:
            raise HTTPException(status_code=400,detail="Agent creation failed.")
        return {"message":f"Mission number {mission["id"]} created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"server error: {e}")
    
@router.put("/{id}/assign/{agent_id}")
def assign_task_to_agent(id:int,agent_id:int):
    try:
        mission = missions_table.get_mission_by_id(id)
        if not mission:
            raise HTTPException(status_code=404,detail=f" Mission: {id} not found")
        
        agent = agent_table.get_agent_by_id(agent_id)
        if not agent:
            raise HTTPException(status_code=404,detail=f"Agent: {agent_id} not found")
        
        if  mission["status"] != "NEW":
            raise HTTPException(status_code=400,detail=f"Mission {id} not available")
        
        if not agent["is_active"]:
            raise HTTPException(status_code=400,detail=f"Agent {agent_id} is not active ")
        
        total_open_mission = missions_table.get_open_missions_by_agent(agent_id)
        if not int(total_open_mission)  < 3:
            raise HTTPException(status_code=400,detail=f"Agent {agent_id} has reached maximum missions ")
        
        if mission["risk_level"] == "HIGH" and agent["agent_rank"]!="Commander":
            raise HTTPException(status_code=400,detail=f"Only Commander can handle critical missions ")
        
        missions_table.assign_mission(id,agent_id)
        missions_table.update_mission_status(id,"IN_PROGRESS")
        return {"message":f"Mission number {mission["id"]} assign to agent {agent_id}"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"server error: {e}")
    
@router.put("/{id}/start")
def update_status_start_mission(id:int):
    try:
        mission = missions_table.get_mission_by_id(id)
        if not mission:
            raise HTTPException(status_code=404,detail=f"id  mission: {id} not found")
        if  mission["status"] != "ASSIGNED":
            raise HTTPException(status_code=400,detail=f"Only mission assigind coul start ")
        missions_table.update_mission_status(id,"IN_PROGRESS")
        return {"message":f"Mission  number {mission["id"]} status update successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"server error: {e}")
    
@router.put("/{id}/complete")
def update_status_complete_mission(id:int):
    try:
        mission = missions_table.get_mission_by_id(id)
        if not mission:
            raise HTTPException(status_code=404,detail=f"id  mission: {id} not found")
        if  mission["status"] != "IN_PROGRESS":
            raise HTTPException(status_code=400,detail=f"Only mission in progress could copleeted ")
        
        missions_table.update_mission_status(id,"COMPLETED")
        agent_table.increment_completed(mission["assigned_agent_id"])
        return {"message":f"Mission  number {mission["id"]} status update successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"server error: {e}")
    
@router.put("/{id}/fail")
def update_status_fail_mission(id:int):
    try:
        mission = missions_table.get_mission_by_id(id)
        if not mission:
            raise HTTPException(status_code=404,detail=f"id  mission: {id} not found")
        if  mission["status"] != "IN_PROGRESS":
            raise HTTPException(status_code=400,detail=f"Only mission in progress could failed ")
        missions_table.update_mission_status(id,"FAILED")
        agent_table.increment_failed(mission["assigned_agent_id"])
        return {"message":f"Mission  number {mission["id"]} status update successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"server error: {e}")
    

@router.put("/{id}/cancel")
def update_status_cancel_mission(id:int):
    try:
        mission = missions_table.get_mission_by_id(id)
        if not mission:
            raise HTTPException(status_code=404,detail=f"id  mission: {id} not found")
        if not mission["status"] in ["NEW","ASSIGNED"]:
            raise HTTPException(status_code=400,detail=f"Only mission NEW OR ASSIGNED could canceled ")
        missions_table.update_mission_status(id,"CANCELLED")
        return {"message":f"Mission  number {mission["id"]} status update successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"server error: {e}")
       

    
    