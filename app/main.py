from fastapi import FastAPI, HTTPException
import uvicorn
from app.classes.prompt_request import PromptRequest
from huggingface_hub import login
import logging
import os
from dotenv import load_dotenv
from app.classes.slonito_model import SlonitoModel

load_dotenv()

login(token = os.getenv("HF_TOKEN"))

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

app = FastAPI()
slonito = SlonitoModel()


@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        logger.debug("Starting generation...")

        response: str = slonito.generate_response(request)

        logger.debug("Generation completed!")

        return {"response": response}
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/marco")
async def marco():
    try:
        return {"response": "polo"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "SLONITO: Up and Running"}
