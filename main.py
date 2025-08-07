import uvicorn
import os
from dotenv import load_dotenv


load_dotenv()

if __name__ == "__main__":
    uvicorn.run("app.main:app",
                port=int(os.getenv("UVICORN_PORT", 4000)),
                log_level=os.getenv("UVICORN_LOG_LEVEL"),
                host=os.getenv("UVICORN_HOST", "0.0.0.0"),
                reload=bool(os.getenv("UVICORN_RELOAD", False)))
