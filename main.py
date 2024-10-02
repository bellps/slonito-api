from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer
from huggingface_hub import login
from local_gemma import LocalGemma2ForCausalLM
import logging
import uvicorn
import torch

login(token = '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')

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

torch.cuda.empty_cache()

model = LocalGemma2ForCausalLM.from_pretrained("google/gemma-2-2b-it", preset="memory", device="cuda")
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b-it")


class PromptRequest(BaseModel):
    prompt: str
    sql_schema: str


def formated_prompt(request):
    return f"""
    You are a relational database specialist, with the focus of creating PostgreSQL queries. Using the SQL schema:
    {request.sql_schema}
    Generate only a SQL query for the following question, no explanation needed:
    {request.prompt}
    """


@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        messages = [
            {"role": "user", "content": formated_prompt(request)},
        ]

        model_inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", return_dict=True).to("cuda")

        logger.debug('Starting generation...')

        generated_ids = model.generate(**model_inputs, max_new_tokens=1024, do_sample=True)
        decoded_text = tokenizer.batch_decode(generated_ids)

        logger.debug('Generation completed!')

        torch.cuda.empty_cache()

        return {"response": decoded_text[0]}
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/marco")
async def marco(request: PromptRequest):
    try:
        return {"response": "polo"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "SLONITO: Up and Running"}


# uvicorn main:app --reload --host 0.0.0.0 --port 4000 --log-level debug
