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

@app.get("/items")
def read_item():
    return {"Items": items}

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return {"Items": items}