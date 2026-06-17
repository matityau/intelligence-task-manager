import mysql.connector

class DB_connection:
    def __init__(self) -> None:
        pass

    def get_connection(self):
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1234",
            database = "Intelligence_db",
            use_pure =True
        )

        return conn
    def create_database(self):
      
            conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="1234",
            use_pure =True)

            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db;")
            conn.commit()
            cursor.close()
            conn.close()
            return "database created"
        
            
    def create_tables(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql_agentes = """CREATE TABLE IF NOT EXISTS agents ( id INT PRIMARY KEY AUTO_INCREMENT,
                            name VARCHAR(50) NOT NULL,
                            specialty VARCHAR(100) NOT NULL,
                            is_active BOOLEAN DEFAULT TRUE,
                            completed_missions INT DEFAULT 0,
                            failed_missions INT DEFAULT 0,
                            agent_rank ENUM('Junior','Senior','Commander') NOT NULL);"""
            
            sql_missions = ("""
                    CREATE TABLE IF NOT EXISTS  missions (id INT PRIMARY KEY AUTO_INCREMENT,
                      title VARCHAR(100) NOT NULL,
                      description TEXT NOT NULL,
                      location VARCHAR(100) NOT NULL,
                      difficulty INT NOT NULL,
                      importance INT NOT NULL,
                      status ENUM('NEW','ASSIGNED','IN_PROGRESS','COMPLETED','FAILED','CANCELLED') DEFAULT "NEW",
                      risk_level VARCHAR(50),
                      assigned_agent_id INT DEFAULT NULL);""")
            
            cursor.execute(sql_agentes)
            cursor.execute(sql_missions)
            conn.commit()
            return {"Tabales create succsesfuly"}
        
        except Exception as e:
            raise e
        finally:
            cursor.close()
            cursor.close()

create_database_and_tables = DB_connection()