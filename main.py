from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging
import sys

app = FastAPI()

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

@app.options("/track")
async def preflight(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "https://dentera.info"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return Response(status_code=204)

class TrackData(BaseModel):
    page: str
    source: Optional[str] = None
    timestamp: Optional[str] = None
    user_agent: Optional[str] = None

@app.post("/track")
async def track(data: TrackData, request: Request):
    ip = request.client.host
    user_agent = request.headers.get("user-agent")
    log_data = {
        "ip": ip,
        "user_agent": user_agent,
        "page": data.page,
        "source": data.source,
        "timestamp": data.timestamp or datetime.now().isoformat()
    }
    logging.info(str(log_data))
    return JSONResponse(content={"status": "ok"}, headers={"Access-Control-Allow-Origin": "https://dentera.info"})

@app.get("/track")
async def test_track():
    return JSONResponse(content={"message": "GET /track is alive"}, headers={"Access-Control-Allow-Origin": "https://dentera.info"})

@app.get("/")
def root():
    return {"message": "up"}