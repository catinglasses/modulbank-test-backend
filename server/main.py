from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException

from server.models.database import init_db
from server.schemas import MessageCreate, MessageResponse
from server.service import MessageService, get_message_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/create-message", response_model=list[MessageResponse])
async def create_message(
    message: MessageCreate,
    message_service: MessageService = Depends(get_message_service)
):
    try:
        new_message = await message_service.create_message(message_create=message)
        messages = await message_service.get_last_messages(10)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
