from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

app = FastAPI()

model_name = "slonito-ai"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)


class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        response = generator(request.prompt, num_return_sequences=1)
        return {"response": response[0]['generated_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "SLONITO: Up and Running"}
