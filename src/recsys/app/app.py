from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/get_recs")
def get_recs():
    pass


if __name__ == "__main__":
    # setup_logging
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)