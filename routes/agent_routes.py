from fastapi import APIRouter,HTTPException
from database.agent_db import agent_table
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)
logging.getLogger("mysql.connector").setLevel(logging.WARNING)

router = APIRouter()

class Agent(BaseModel):
    name:str
    specialty:str
    agent_rank:str

class UpdateAgent(BaseModel):
    name: Optional[str]
    specialty: Optional[str]
    agent_rank:str

@router.get("")
def get_all_agents():
    try:
        logger.info("GET/ agents called ")
        all = agent_table.get_all_agents()
        if not all:
            return []
        return all
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error: {e}")


@router.get("/{id}")
def get_agent_by_id(id:int):
    try:
        logger.info("GET/ agents/{id} called ")
        agent = agent_table.get_agent_by_id(id)
        if not agent:
            raise HTTPException(status_code=404,detail=f"id agent: {id} not found")
        return agent
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error: {e}")


@router.post("",status_code=201)
def create_agent(data:Agent):
    try:
        logger.info("POST/ agents called")
        if not data:
            raise HTTPException(status_code=400,detail=f"DATA not filed")
        
        if not data.agent_rank in ['Junior','Senior','Commander']:
            raise HTTPException(status_code=400,detail="Agent rank must be 'Junior'/'Senior'/'Commander'.")
        
        data_dict = data.model_dump()
        agent = agent_table.create_agent(data_dict)

        if not agent:
            raise HTTPException(status_code=400,detail="Agent creation failed.")
        return {"message":f"Agent number {agent["id"]} created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"server error: {e}")
        
@router.put("/{id}")
def update_agent(id:int,data:UpdateAgent):
    try:
        logger.info("PUT/ agents/{id} called ")
        agent = agent_table.get_agent_by_id(id)
        if not agent:
            raise HTTPException(status_code=404,detail=f"Agent {id} not found")
        if not data:
            raise HTTPException(status_code=400,detail=f"DATA not filed")
        
        if not data.agent_rank in ['Junior','Senior','Commander']:
            raise HTTPException(status_code=400,detail="Agent rank must be 'Junior'/'Senior'/'Commander'.")
        
        data_dict = data.model_dump(exclude_none=True)
        success = agent_table.update_agent(id,data_dict)
        if not success:
            raise HTTPException(status_code=400,detail=f"update agenet {id} failed")
        return {"message":f"Agent id: {id} update successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"server error: {e}")

@router.put("/{id}/deactivate")
def deactivate_agent(id:int):
    try:
        logger.info("PUT/ agents/{id}/deactivate called ")
        agent = agent_table.get_agent_by_id(id)
        if not agent:
            raise HTTPException(status_code=404,detail=f"Agent {id} not found")
        if not agent["is_active"]:
            raise HTTPException(status_code=400,detail=f"Agent {id} is already deactivate")
        agent_table.deactivate_agent(id)
        
        return {"message":f"Agent id: {id} deactivate successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"server error: {e}")

@router.get("/{id}/performance")
def get_agent_performance(id:int):
    try:
        logger.info("GET/ agents/{id}/performance called ")
        agent = agent_table.get_agent_by_id(id)
        if not agent:
            raise HTTPException(status_code=404,detail=f"Agent {id} not found")
        performance = agent_table.get_agent_performance(id)
        return performance
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"server error: {e}")


# data_dict = data.model_dump(exclude_none=True)
# keys = ", ".join([f'{key}=%s' for key in data_dict.keys()])    
