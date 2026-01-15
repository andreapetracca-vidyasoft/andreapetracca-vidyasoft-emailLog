from fastapi import FastAPI
from app.pkg.controller.Controller import router

app = FastAPI()

@app.get("/")
async def We_Good() -> dict:
    return {"status": "ok"}

app.include_router(router)
