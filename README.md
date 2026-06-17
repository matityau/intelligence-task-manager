# intelligence-task-manager

## System description
This system is designed for managing intelligence tasks that manages agents and tasks by task level and according to the agent's suitability for the task.

In this system, you can add new agents, get information about all agents or get information about a specific agent. Furthermore, you can get general information about the status of the tasks that have been performed, how many of them failed and how many succeeded.
The cart is connected to the database and updates the data into it using the Python language which connects them in Mysql


## Folder structure
```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore 
```

## Tabales description
### agents
```
Field _______________Type _______________Notes_________________________
id____________________INT__________AUTO_INCREMENT, PK
____________________________________________________________________	
name_________________VARCHAR_______________________________________
____________________________________________________________________	
specialty____________VARCHAR
____________________________________________________________________	
is_active____________BOOLEAN________DEFAOULT TRUE
____________________________________________________________________
completed_missions_____INT_________DEFAOULT 0
____________________________________________________________________
failed_missions________INT	_________DEFAOULT 0
____________________________________________________________________
agent_rank___ENUM / VARCHAR	____only:'Junior' / 'Senior' / 'Commander' 
____________________________________________________________________
```

### missions
```
Field _______________Type _______________Notes_________________________
id------------------- INT-----------AUTO_INCREMENT, PK Unique identifier
____________________________________________________________________
title-------------- VARCHAR---------Task title
____________________________________________________________________
description---------- TEXT ---------Detailed description
____________________________________________________________________
location------- -----VARCHAR --------Location
____________________________________________________________________
difficulty------------ INT--------- 1–10 only
____________________________________________________________________
importance------------ INT--------- 1–10 only
____________________________________________________________________
status-------------- VARCHAR-------Default: NEW
____________________________________________________________________
risk_level----------- VARCHAR------ Automatically calculated — not from user
____________________________________________________________________
assigned_agent_id------INT-------- NULL until assigned
____________________________________________________________________
```

## Explanation of departments
### DB_connection
```
Method________________________Function______________________

get_connection()----- returns an active connection to MySQL
create_database()---- creates Intelligence_db if it does not exist
create_tables()------- creates both tables if they do not exist

The create_database and create_tables functions will run when the system boots.

```
_____________________________________________________________________________
## AgentDB
```
Method_________________________Function______________________
create_agent(data)            |creates a new agent and returns the agent object
_____________________________________________________________________________
get_all_agents()              |returns a list of all agents
_____________________________________________________________________________
get_agent_by_id(id)           | returns one agent by ID, or None
_____________________________________________________________________________
update_agent(id, data)        | UPDATE the entire row (id cannot be changed)
_____________________________________________________________________________
deactivate_agent(id)          | sets the agent to inactive
_____________________________________________________________________________
increment_completed(id)       |updates the number of completed tasks
_____________________________________________________________________________
increment_failed(id)          |updates the number of failed tasks
_____________________________________________________________________________
get_agent_performance(id)     | returns a dictionary with these keys completed, failed, total, success_rate
                              | (note that calculating this value success_rate - what percentage of tasks completed successfully out of the total)
_____________________________________________________________________________
count_active_agents()         | returns the number of active agents
_____________________________________________________________________________
```

## MissionDB
```
Method____________________________________________Function    ______________________
create_mission(data)           | Creates a new mission and returns the entire object
____________________________________________________________________________________
get_all_missions()             |returns all missions
____________________________________________________________________________________
get_mission_by_id(id)          | returns a single mission by ID, or None
____________________________________________________________________________________
assign_mission(m_id, a_id)     | Assigns a mission to an agent
____________________________________________________________________________________
update_mission_status(id, status)| Used for any status change
____________________________________________________________________________________
get_open_missions_by_agent(id)  |Returns ASSIGNED/IN_PROGRESS missions of an agent
____________________________________________________________________________________
count_all_missions()           |Total missions
____________________________________________________________________________________
count_by_status(status)        | Counts by a specific status
____________________________________________________________________________________
count_open_missions()          | Counts open missions
____________________________________________________________________________________
count_critical_missions()      | Counts CRITICAL missions
____________________________________________________________________________________
get_top_agent()                | The agent with the highest completed_missions
____________________________________________________________________________________
```

## System rules

```
1 rank must be 'Junior' / 'Senior' / 'Commander' — any other value throws an error.
2 difficulty and importance must be between 1 and 10 — otherwise an error.
3 risk_level is calculated automatically when creating a task — the user does not submit it.
4 An agent with is_active=False cannot accept tasks.
5 An agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.
6 If risk_level=CRITICAL — only an agent with the Commander rank can accept the task.
7 Only a task with the status NEW can be assigned. After assignment: status=ASSIGNED.
8 Only a task with the status ASSIGNED can be started. After: status=IN_PROGRESS.
9 Only a task with the status IN_PROGRESS can be finished and changed to failed or completed.
10 Only a task with the status NEW or ASSIGNED can be canceled — otherwise an error.
```

## Running instructions

 - docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
 - python -m venv venv
 - ./venv/Scripts/Activate
 - pip install -r requirements.txt
 - python main.py