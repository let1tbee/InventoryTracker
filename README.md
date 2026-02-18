**Project info:**
* **Docker images:** postgres:alpine, dpage/pgadmin4
* **Python libraries:** SQLAlchemy, FastAPI, Pydantic

**Prerequirements:**
* Installed Docker

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

**Endpoints:**
* url: http://localhost:8000/
* /docs - FastAPI documentation GUI
* get: / - "Hello world"

**Structure:**
InventoryTracker/
├──app/
│  ├──api/\
│     ├──employees.py
│     └──equipment.py
│  ├──env/
│     ├──.env
│     └──.env.db
│  ├──repository/
│     ├──employees.py
│     └──equipment.py
│  ├──models.py
│  ├──main.py
│  ├──docker-compose.yaml
│  ├──README.md
│  ├──requirements.txt