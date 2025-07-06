from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
from datetime import datetime

# Логирование в файл + консоль
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # поменяй на домен сайта при необходимости
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель данных
class TrackData(BaseModel):
    source: Optional[str] = None
    timestamp: Optional[str] = None
    page: Optional[str] = None

# Проверка сервиса
@app.get("/")
def root():
    return {"message": "Service is working"}

# Обработка трекинга
@app.post("/track")
async def track_endpoint(data: TrackData, request: Request):
    ip = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")
    timestamp = data.timestamp or datetime.now().isoformat()

    log_entry = (
        f"🔹 Tracking Event:\n"
        f"Page: {data.page}\n"
        f"Source: {data.source}\n"
        f"Timestamp: {timestamp}\n"
        f"IP: {ip}\n"
        f"User-Agent: {user_agent}\n"
        "--------------------------------------"
    )

    logger.info(log_entry)

    return {"status": "success", "logged": True}