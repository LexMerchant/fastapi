from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging
import json

app = FastAPI()

# Включаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("tracking.log"), logging.StreamHandler()]
)

class TrackData(BaseModel):
    source: Optional[str] = None
    timestamp: Optional[str] = None
    page: str

@app.get("/")
def read_root():
    return {"message": "Service is working"}

@app.post("/track")
async def track(data: TrackData, request: Request):
    log_entry = {
        "ip": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "timestamp": data.timestamp or datetime.utcnow().isoformat(),
        "source": data.source,
        "page": data.page,
        "method": request.method,
        "path": request.url.path,
        "referrer": request.headers.get("referer")
    }
    logging.info(json.dumps(log_entry, ensure_ascii=False))
    return {"status": "ok"}
