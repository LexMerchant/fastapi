from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging

app = FastAPI()

# Настройка логгирования
logging.basicConfig(
    filename="track.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Разрешаем CORS только с твоего сайта (обязательно без / в конце!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dentera.info"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель данных
class TrackData(BaseModel):
    page: str
    source: Optional[str] = None
    timestamp: Optional[str] = None
    user_agent: Optional[str] = None

# Обработчик трека
@app.post("/track")
async def track(data: TrackData, request: Request):
    ip = request.client.host
    user_agent = request.headers.get("user-agent")
    log_entry = {
        "ip": ip,
        "user_agent": user_agent,
        "page": data.page,
        "source": data.source,
        "timestamp": data.timestamp or datetime.now().isoformat()
    }
    logging.info(str(log_entry))
    return {"status": "ok"}

# Тестовая ручка
@app.get("/")
def read_root():
    return {"message": "Service is working"}