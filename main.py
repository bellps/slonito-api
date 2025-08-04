import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=4000, log_level="debug", host="0.0.0.0", reload=True)
