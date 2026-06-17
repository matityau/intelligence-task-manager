import mysql.connector
from database.db_connection import DB_connection

connect = DB_connection()

class AgentDB:
    def __init__(self) -> None:
        pass

    def create_agent(self,data):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql_create = """INSERT INTO agents (name,specialty,is_active,completed_missions,failed_missions,agent_rank)
                            VALUES(%s,%s,%s,%s,%s,%s);"""
            values = (data[""],data[""],data[""],data[""])

    
    def get_all_agents(self):
        conn =  
        pass
    def get_agent_by_id(self,id):
        pass
    def update_agent(self,id, data):
        pass
    def deactivate_agent(self,id):
        pass
    def increment_completed(self,id):
        pass
    def increment_failed(self,id):
        pass
    def get_agent_performance(self,id):
        pass
    def count_active_agents(self):
        pass

