import mysql.connector
from database.db_connection import DB_connection
connect = DB_connection()

class MissionDB:
    def __init__(self) -> None:
        pass

    def calculate_risk_level(self,risc):
        if 0 <= risc <= 9:
            return "LOW"
        elif 10 <= risc <= 17:
             return "MEDIUM"
        elif 18 <= risc <= 24:
            return "HIGH"
        elif  risc >= 25:
            return "CRITICAL"
        
    def create_mission(self,data:dict):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            risc_intenger = int(data["difficulty"]) * 2 + int(data["importance"])
            risc_words =self.calculate_risk_level(risc_intenger)

            sql_create = """INSERT INTO missions (title,description,location,difficulty,importance,risk_level)
                            VALUES(%s,%s,%s,%s,%s,%s);"""
            values = (data["title"],data["description"],data["location"],data["difficulty"],data["importance"],risc_words)
            cursor.execute(sql_create,values)
            conn.commit()
            new_id = cursor.lastrowid
            cursor.execute("SELECT * FROM missions WHERE id = %s;",(new_id,))
            mission = cursor.fetchone()
            return mission
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()
        
 
    def get_all_missions(self):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM missions;")
            rows = cursor.fetchall()
            if not rows:
                return []
            return rows
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_mission_by_id(self,id:int):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM missions WHERE id = %s;",(id,))
            row = cursor.fetchone()
            if not row:
                return []
            return row
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def assign_mission(self,m_id, a_id)->bool:
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql ="UPDATE missions SET assigned_agent_id=%s WHERE id=%s"
            cursor.execute(sql,(a_id,m_id))
            conn.commit()           
            row = cursor.rowcount
            return row > 0
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def update_mission_status(self,id:int, status:str)->bool:
        try:
            if not status in ['NEW','ASSIGNED','IN_PROGRESS','COMPLETED','FAILED','CANCELLED']:
                raise ValueError
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql ="UPDATE missions SET status = %s WHERE id=%s"
            cursor.execute(sql,(status,id,))
            conn.commit()           
            row = cursor.rowcount
            return row > 0
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_open_missions_by_agent(self,id:int):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql ="SELECT * FROM missions WHERE assigned_agent_id=%s"
            cursor.execute(sql,(id,))         
            rows = cursor.fetchall()
            return rows
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def count_all_missions(self):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT count(*) AS total FROM missions;")
            row = cursor.fetchone()
            return row["total"]
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def count_by_status(self,status):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT count(*) AS total FROM missions WHER status=%s;",(status,))
            row = cursor.fetchone()
            return {status : row["total"]}
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close() 

    def count_open_missions(self):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT count(*) AS total FROM missions WHER status = 'IN_PROGRESS';")
            row = cursor.fetchone()
            return {"open missions" : row["total"]}
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()  

    def count_critical_missions(self):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT count(*) AS total FROM missions WHER risk_level = 'CRITICAL';")
            row = cursor.fetchone()
            return {"CRITICAL missions" : row["total"]}
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()  

    def get_top_agent(self):
        try:
            conn = connect.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM agents ORDER BY completed_missions DESC LIMIT 1;")
            row = cursor.fetchone()
            return {"Top agent" : row["name"]}
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close() 




#  def assign_mission(self, m_id: int, a_id: int):
#         mission = self.get_mission_by_id(m_id)
#         agent = agent_db.get_agent_by_id(a_id)

#         if not mission or not agent:
#             raise ValueError("Mission or Agent not found.")
#         if mission["status"] != "NEW":
#             raise ValueError("Can only assign a mission with 'NEW' status.")
#         if not agent["is_active"]:
#             raise ValueError("Inactive agent cannot receive missions.")
        
#         open_missions = self.get_open_missions_by_agent(a_id)
#         if len(open_missions) >= 3:
#             raise ValueError("Agent cannot hold more than 3 open missions.")
#         if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
#             raise ValueError("CRITICAL missions can only be assigned to a Commander.")

#   conn = db_manager.get_connection()
#         cursor = conn.cursor()
#         cursor.execute("UPDATE missions SET assigned_agent_id = %s, status = 'ASSIGNED' WHERE id = %s", (a_id, m_id))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return {"status": "success", "message": "Mission assigned successfully"}





missions_table = MissionDB()