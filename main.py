from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def hello():
    return {"hello": "world"}
