**Project info:**
* **Docker images:** postgres:alpine, dpage/pgadmin4
* **Python libraries:** SQLAlchemy, FastAPI, Pydantic

**Prerequirements:**
* Installed Docker

**Setup:**
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
* url: localhost:8000/
* get: / - "Hello world" 
* get: /items - Returns item by ID
* post: /items - Adds item to a list
* /docs - FastAPI documentation GUI