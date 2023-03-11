from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "FastAPI test in swarm02 by Bundit Songpracha SPCN26"}