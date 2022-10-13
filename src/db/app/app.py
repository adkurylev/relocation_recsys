from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.post("/add_user")
def add_user():
    pass

@app.get("/get_user")
def get_user():
    pass

@app.post("/add_city")
def add_city():
    pass

@app.get("/get_city")
def get_city():
    pass


if __name__ == "__main__":
    # setup_logging
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)

