from uuid import UUID
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from server.models.database import Base

class Message(Base):
    """Represent a message in the system database."""
    __tablename__ = "messages"

    message_id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    sender: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(default="foobar")
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
    serial_number: Mapped[int] = mapped_column(unique=True)
    user_count: Mapped[int] = mapped_column(nullable=False)
