from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()

class TrackData(BaseModel):
    source: Optional[str] = None
    timestamp: str
    page: str

@app.post("/track")
async def track(data: TrackData):
    print(f"Received data: {data}")
    return {"status": "success", "received": data}

@app.get("/")
async def root():
    return {"message": "Service is working"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
