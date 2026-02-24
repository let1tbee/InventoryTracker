**Project info:**

**Description**

This project is a demo version of backend functionality for corporate inventory tracker app.
The main purpose of which is to keep employee and equipment database and to assign equipment for dedicated employee.
The app supports login functionality with separate user SQL table.
The database has been put into Docker container and creates separate volume in order to keep the data integrity between app executions.
The app also includes positive unit tests, split into a logic modules. The tests utilize independent temporary SQLite table and could be run without Docker container.

Additional API features:
* For both equipment and employees: add, get singular result, get multiple results, modify and delete entry.
* Search for specific entries, e.g. get all available equipment.
* Assign multiple equipment to an employee.
* Get all assigned equipment.

Additional info:
* **Docker images:** postgres:alpine, dpage/pgadmin4
* **Python backend libraries:** FastAPI, SQLModel (SQLAlchemy, Pydantic)

**Prerequirements:**
* Installed Docker
* Installed Browser
* Installed python and libraries from requirements.txt
* fill .env files with your data and remove ".example" from file names

**Setup:**
* pip install -r requirements.txt
* run "docker compose up -d"
* uvicorn main:app --reload
* To obtain access for locked behind login options use Users and post username and password.
* Add employee and equipment entity because app starts with empty database

**DOCKER commands:**
* docker compose up -d
* docker compose down

**pgadmin4:**
* Access via http://localhost:5050/ link
* Credentials located in ".env.db"

**FastAPI commands:**
* uvicorn main:app --reload

**pytest commands**
* detailed: pytest -v -s
* debug: pytest -x -v -l

**LINKS:**
* http://localhost:8000/ - base API url
* http://localhost:8000/docs - Swagger documentation GUI


**Structure:**
```text
InventoryTracker/
├── app/                    
│   ├── api/                # directory with routes
│   │   ├── employees.py    
│   │   ├── equipment.py    
│   │   └── login.py        
│   ├── env/                 
│   │   ├── .env            # secrets for app setup 
│   │   └── .env.db         # secrets for database and docker setup 
│   ├── repository/         # directory with crud operations connected to routes
│   │   ├── employees.py    
│   │   ├── equipment.py    
│   │   └── login.py        
│   ├── config.py           # configurational variables setup
│   ├── database.py         # database setup
│   ├── models.py           # SQLModel models
│   └── oauth2.py           # OAuth2 functions with JWT
├── tests/                  # directory with module tests
│   ├── test_default.py     
│   ├── test_employees.py   
│   └── test_equipment.py   
├── .gitignore              # git config file
├── conftest.py             # pytest general file with fixtures
├── docker-compose.yaml     # docker setup script
├── main.py                 # main app file
├── README.md               
└── requirements.txt        # python dependencies list
```
