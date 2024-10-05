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
    {instructions()}
    Using the SQL schema:
    {request.sql_schema}
    Generate a SQL query for the following question:
    {request.prompt}
    """

def instructions():
    return f"""
    # System Instructions

    ## Basic Rules
    You are a relational database specialist, with the focus of creating SQL queries based on a given database schema and a question from the user.

    Your output must fit following markdown format:
    ```sql
        query
    ```
    , where "query" must be replaced by the query that you created.

    The queries must follow the PostgreSQL dialect.
    If the question does not match the database schema by any chance, you must output an empty string, without the markdown format.
    
    <end_of_turn><start_of_turn>user
    """

@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        messages = [
            {"role": "user", "content": formated_prompt(request)},
        ]

        logger.debug('Starting generation...')

        model_inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt", return_dict=True).to("cuda")
        generated_ids = model.generate(**model_inputs, max_new_tokens=1024, do_sample=True)
        decoded_text = tokenizer.batch_decode(generated_ids, clean_up_tokenization_spaces=True)

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
