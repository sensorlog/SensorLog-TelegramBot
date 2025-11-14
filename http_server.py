"""
SensorLog-TelegramBot

Este script recebe os dados enviados por http_post.py.
"""

from fastapi import FastAPI, Request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/events")
async def receive_event(request: Request):
    data = await request.json()
    logger.info("Evento recebido: %s", data)
    return {"success": True}


@app.post("/values")
async def receive_values(request: Request):
    data = await request.json()
    logger.info("Valores recebidos: %s", data)
    return {"success": True}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9001)
