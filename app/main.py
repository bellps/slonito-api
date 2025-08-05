from fastapi import FastAPI
from huggingface_hub import login
import os
from .routers import main

login(token = os.getenv("HF_TOKEN"))

app = FastAPI()
app.include_router(main.router)

@app.get("/")
async def root():
    return {"message": "SLONITO: Up and Running"}
