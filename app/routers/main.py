from fastapi import APIRouter, HTTPException
import logging

from app.types.prompt_request import PromptRequest
from app.classes.slonito_model import SlonitoModel


router = APIRouter()
slonito = SlonitoModel()

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

@router.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        logger.debug("Starting generation...")

        response: str = slonito.generate_response(request)

        logger.debug("Generation completed!")

        return {"response": response}
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=500, detail=str(e))
