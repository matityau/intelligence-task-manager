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
            sql_create = """INSERT INTO agents (name,specialty,agent_rank) VALUES (%s,%s,%s);"""
            values = (data["name"],data["specialty"],data["agent_rank"])
            cursor.execute(sql_create,(values))
            conn.commit()
            new_id = cursor.lastrowid
            agent = self.get_agent_by_id(new_id)
            return agent
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    

    
    def get_all_agents(self):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM agents;")
            rows = cursor.fetchall()
            if not rows:
                return []
            return rows
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_agent_by_id(self,id:int):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM agents WHERE id = %s;",(id,))
            row = cursor.fetchone()
            if not row:
                return []
            return row
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    
    def update_agent(self, agent_id: int, data: dict):
        conn = connect.get_connection()
        cursor = conn.cursor()
        sql_update = """
        UPDATE agents 
            SET name = %s, specialty = %s, agent_rank = %s WHERE id = %s;"""
        values = (data["name"], data["specialty"],data["agent_rank"],agent_id)
        cursor.execute(sql_update,values )
        conn.commit()

        success = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return {"status": "success" if success else "failed"}
    
    def deactivate_agent(self,id:int)->bool:
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql ="UPDATE agents SET is_active=FALSE WHERE id=%s"
            cursor.execute(sql,(id,))
            conn.commit()           
            row = cursor.rowcount
            return row > 0
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()
        
    def increment_completed(self,id:int):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql ="UPDATE agents SET completed_missions = completed_missions + 1 WHERE id=%s"
            cursor.execute(sql,(id,))
            conn.commit()           
            row = cursor.rowcount
            return row > 0
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()
            
    def increment_failed(self,id:int):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql ="UPDATE agents SET failed_missions = failed_missions + 1 WHERE id=%s"
            cursor.execute(sql,(id,))
            conn.commit()           
            row = cursor.rowcount
            return row > 0
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_agent_performance(self,id:int):
       
        agent = self.get_agent_by_id(id)
        if  agent:
            comp = agent["completed_missions"]
            fail = agent["failed_missions"]
            total = comp + fail
            success_rate = (comp / total * 100) if total > 0 else 0
            return {"completed": comp, "failed": fail, "total": total, "success_rate": success_rate}
        return None
        

    def count_active_agents(self):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) FROM agents WHERE is_active = TRUE")
            row = cursor.fetchone()[1]
            cursor.close()
            conn.close()
            return row
        
        except Exception as e:
            raise e
        
            


agent_table = AgentDB()


