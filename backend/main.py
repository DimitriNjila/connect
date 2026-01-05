import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from fastapi import HTTPException


class Fruit(BaseModel):
    id: str
    name: str
    color: str


class FruitInput(BaseModel):
    name: str
    color: str


class Fruits(BaseModel):
    fruits: List[Fruit]


app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"fruits": []}


@app.get("/fruits", response_model=Fruits)
def get_fruits():
    return Fruits(fruits=memory_db["fruits"])


@app.post("/fruits", response_model=Fruit)
def add_fruit(payload: FruitInput):
    fruit = Fruit(id=str(uuid4()), name=payload.name, color=payload.color)
    memory_db["fruits"].append(fruit)
    return fruit


@app.delete("/fruits/{fruit_id}", response_model=Fruits)
def delete_fruit(fruit_id: str):
    if not any(fruit.id == fruit_id for fruit in memory_db["fruits"]):
        raise HTTPException(status_code=404, detail="Fruit not found")
    memory_db["fruits"] = [
        fruit for fruit in memory_db["fruits"] if fruit.id != fruit_id
    ]
    return Fruits(fruits=memory_db["fruits"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
