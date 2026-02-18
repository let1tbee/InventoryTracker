from fastapi import FastAPI
from app.api import employees
from app.database import lifespan

TITLE = "Inventory Tracker"
DESCRIPTION = "A tool that is used to track equipment within the company."
SUMMARY = "Backend portfolio project."
VERSION = '0.0.1'

app = FastAPI(title=TITLE,
              description=DESCRIPTION,
              summary=SUMMARY,
              version=VERSION,
              lifespan=lifespan)

app.include_router(employees.router)

@app.get("/")
def read_root():
    return {"Welcome to Inventory Tracker API!"}
