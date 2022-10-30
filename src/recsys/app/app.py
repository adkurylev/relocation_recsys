from fastapi import FastAPI
import uvicorn
import argparse
from pydantic import BaseModel
import random

app = FastAPI()


class User(BaseModel):
    tg_id: int


@app.get("/recommendation")
def get_recs():

    return {"city_id": str(random.randint(100, 500)),
            "city_name": "The best city",
            "description": "city_description"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, dest="port")
    parser.add_argument("--host", default="0.0.0.0", type=str, dest="host")
    parser.add_argument("--debug", action="store_true", dest="debug")
    args = vars(parser.parse_args())

    uvicorn.run(app, **args)
    #@TODO setup_logging
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)