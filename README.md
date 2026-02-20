**Project info:**
* **Docker images:** postgres:alpine, dpage/pgadmin4
* **Python libraries:** SQLAlchemy, FastAPI, Pydantic

**Prerequirements:**
* Installed Docker
* save .env file as .env
* create .env.db file

**Setup:**
* pip install -r requirements.txt
* run "docker compose up -d"
* uvicorn main:app --reload

**DOCKER commands:**
* docker compose up -d
* docker compose down

**pgadmin4:**
* Access via localhost:5050
* Database name "database"
* Credentials located in ".env.db"

**FastAPI commands:**
* uvicorn main:app --reload

**pytest commands**
* detailed: pytest -v -s
* debug: pytest -x -v -l

**Endpoints:**
* url: http://localhost:8000/
* /docs - FastAPI documentation GUI
* get: / - "Hello world"

**Structure:**
```text
InventoryTracker/
├── app/                    # 
│   ├── api/                # 
│   │   ├── employees.py    # 
│   │   └── equipment.py    # 
│   ├── env/                # 
│   │   ├── .env            # 
│   │   └── .env.db         # 
│   ├── repository/         # 
│   │   ├── employees.py    # 
│   │   └── equipment.py    # 
│   ├── database.py         # 
│   ├── models.py           # 
├── tests/                  # 
│   ├── test_default.py     # 
│   └── test_employees.py   # 
├── main.py                 # 
├── docker-compose.yaml     # 
├── requirements.txt        # 
└── README.md               # 
```
