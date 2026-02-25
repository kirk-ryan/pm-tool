import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/api/test")
async def test_api():
    return {"message": "API is working", "status": "success"}


if os.path.isdir("frontend_out"):
    app.mount("/", StaticFiles(directory="frontend_out", html=True), name="static")
