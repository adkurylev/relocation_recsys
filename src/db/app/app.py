from fastapi import FastAPI
import uvicorn
import argparse
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI()

from db import DBDriver


class User(BaseModel):
    tg_id: int

class Reaction(BaseModel):
    city_id: int
    score: int
    tg_id: int


@app.post("/user")
def add_user(request: User):
    driver = DBDriver()
    driver.add_user(request)
    # check status and return reply
    return {"message": "fine"}

@app.get("/get_user")
def get_user():
    pass

@app.post("/add_city")
def add_city():
    pass

@app.get("/get_city")
def get_city():
    pass

@app.post("/reaction")
def add_reaction(request: Dict[Any, Any]):
    driver = DBDriver()
    driver.add_reaction(**request)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, dest="port")
    parser.add_argument("--host", default="0.0.0.0", type=str, dest="host")
    parser.add_argument("--debug", action="store_true", dest="debug")
    args = vars(parser.parse_args())

    # setup_logging
    uvicorn.run(app, **args)

