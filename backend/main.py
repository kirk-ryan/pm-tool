import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from db import get_board, init_db, set_board


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


# --- models ---

class BoardData(BaseModel):
    columns: list
    cards: dict


# --- API routes ---

@app.get("/api/test")
async def test_api():
    return {"message": "API is working", "status": "success"}


@app.get("/api/board")
async def read_board():
    data = get_board("user")
    if data is None:
        raise HTTPException(status_code=404, detail="Board not found")
    return data


@app.put("/api/board", status_code=204)
async def write_board(body: BoardData):
    ok = set_board("user", body.model_dump())
    if not ok:
        raise HTTPException(status_code=404, detail="Board not found")


# --- static files (frontend) ---

if os.path.isdir("frontend_out"):
    app.mount("/", StaticFiles(directory="frontend_out", html=True), name="static")
