import uvicorn

if __name__ == "__main__":
    uvicorn.run("event_manager.main:app", host="localhost", port=8081, reload=True)
