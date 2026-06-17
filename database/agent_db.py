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
            values = (data["name"],data["specialty"],True,0,0,data["agent_rank"])
            cursor.execute(sql_create,values)
            conn.commit()
            new_id = cursor.lastrowid
            cursor.execute("SELECT * FROM agents WHERE id = %s;",(new_id,))
            agent = cursor.fetchone()
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

    def update_agent(self,id:int, data:dict)->bool:
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            sql ="UPDATE agent SET name=%s,specialty=%s,agent_rank=%s WHERE id=%s"
            values = (data["name"],data["specialty"],data["agent_rank"],id)
            cursor.execute(sql,values)
            conn.commit()           
            row = cursor.rowcount
            return row > 0
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()
        
    def deactivate_agent(self,id:int)->bool:
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql ="UPDATE agent SET is_active=FALSE WHERE id=%s"
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
            sql ="UPDATE agent SET completed_missions = completed_missions + 1 WHERE id=%s"
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
            sql ="UPDATE agent SET failed_missions = failed_missions + 1 WHERE id=%s"
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
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM agents WHERE id;",(id,))
            row = cursor.fetchone()
            completed = int(row["completed_missions"])
            failed = int(row["failed_missions"])
            total_missions = completed + failed
            success_precent =(completed // total_missions)


            return{"completed":completed,
                   "failed":failed,
                   "total":total_missions,
                   "rate_success":f'{success_precent}%'}
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def count_active_agents(self)->int:
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT count(*) AS total FROM agents WHERE is_active = TRUE;")
            row = cursor.fetchall()
            return row["total"]
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

agent_table = AgentDB()


