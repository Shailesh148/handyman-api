# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Docker + Uvicorn + GitHub Actions!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}