<span>
  <img alt="Slonito" width="100%" align="center" src="https://github.com/user-attachments/assets/a32a0822-804c-4ca8-9600-eff1fd45eef9" />
</span>

# 🐘 What is Slonito?

Slonito is a lightweight assistant that helps users generate PostgreSQL queries from natural language prompts. It was developed as part of an academic research project, aiming to support professionals with limited SQL knowledge in creating customized queries with greater speed, accuracy, and confidence.

Slonito API is the backend service responsible for converting natural language prompts into PostgreSQL queries using a fine-tuned Large Language Model (LLM). Built with Python and FastAPI, this API powers the query-generation logic for the Slonito frontend.

> 🧠 The model was fine-tuned using Gemma 2 2B, optimized to handle SQL generation with accuracy and low resource usage.

## Features

🤖 Generates PostgreSQL queries from natural language

🧠 Fine-tuned LLM using supervised learning techniques

⚙️ Modular and language-agnostic – can be reused in other projects

🚀 Built with FastAPI for performance and simplicity

🔐 Designed for local or private server use – ideal for sensitive data

## Tech Stack

- Python 3.10+

- FastAPI

- Hugging Face Transformers

- local-gemma (optimized for local inference)

- PyTorch

- Uvicorn

## Requirements

- CUDA-compatible GPU (recommended for inference)
  - **CUDA Toolkit 12.9**

- Python 3.10+

- Access to the fine-tuned model or the base model (gemma-2-2b-it)

## Setup

```bash
git clone https://github.com/bellps/slonito-api.git
cd slonito-api
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 3001
```

### Environment Variables

Create a .env file or export:

```txt
HF_TOKEN="your_hf_token"
HF_MODEL="google/gemma-2-2b-it"
HF_TOKENIZER="google/gemma-2-2b-it"
```

> [!IMPORTANT]
> If you’re using local-gemma, make sure your GPU drivers and CUDA are properly set up.

## API Endpoint

```txt
POST /generate
```

Request body:

```json
{
  "prompt": "List the names of all employees with salary above 50000.",
  "sql_schema": "CREATE TABLE employees (id INT, name TEXT, salary INT);"
}
```

Response:

```json
{
  "response": "```sql\nSELECT name FROM employees WHERE salary > 50000;\n```"
}
```

# Related Repositories

[Slonito (Rails)](https://github.com/bellps/slonito) – Web interface for interacting with this API.

# 🐘 Who is Slonito?

Slonito is a pink elephant who loves SQL and decided to help every one that's facing trouble with this language ♥️. His name comes from Slonik, the official elephant mascot of PostgreSQL. In Russian, "slonik" means “little elephant”, so the project took that idea a step further by adding the Portuguese diminutive suffix "-ito", commonly used to describe something very small or cute.

So, Slonito is like saying “a tiny, tiny elephant” — a playful nod to the project’s lightweight nature and its connection to PostgreSQL. It’s small, helpful, and works hard behind the scenes to make your life with SQL just a bit easier. 🐘✨
