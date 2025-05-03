from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from server.schemas import MessageCreate
from server.models.database import get_db
from server.models.message import Message

class MessageService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def _get_next_serial_number(self) -> int:
        stmt = select(func.max(Message.serial_number))
        result = await self.db_session.execute(stmt)
        max_serial = result.scalar()

        return 1 if max_serial is None else max_serial + 1

    async def _get_user_message_count(self, sender: str) -> int:
        stmt = select(func.count()).where(Message.sender == sender)
        result = await self.db_session.execute(stmt)

        return result.scalar() or 0

    async def get_last_messages(self, limit: int = 10) -> list[Message]:
        result = await self.db_session.execute(
            select(Message)
            .order_by(Message.serial_number.desc())
            .limit(limit)
        )
        messages = result.scalars().all()
        return sorted(messages, key=lambda m: m.serial_number)

    async def create_message(self, message_create: MessageCreate) -> Message:
        async with self.db_session.begin():
            serial_number = await self._get_next_serial_number()
            user_count = await self._get_user_message_count(message_create.sender) + 1

            message = Message(
                sender=message_create.sender,
                text=message_create.text,
                serial_number=serial_number,
                user_count=user_count
            )

            self.db_session.add(message)
            try:
                await self.db_session.flush()
            except IntegrityError as e:
                await self.db_session.rollback()
                raise ValueError("Failed to create message due to conflict") from e
            
            return message

async def get_message_service(
        db: AsyncSession = Depends(get_db)
) -> MessageService:
    return MessageService(db)
