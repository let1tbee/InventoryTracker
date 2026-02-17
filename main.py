from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

items = []

class Item(BaseModel):
    name: str
    quantity: int = 1

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items")
def create_item(item: str):
    items.append(item)
    return {"Items": items}

@app.get(f"/items/{id}")
def read_item(id: int)-> dict:
    return {"Items": items[id]}

