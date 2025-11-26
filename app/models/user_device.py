from sqlalchemy import (
    Column, BigInteger, String, Text, Boolean, DateTime, ForeignKey, func
)
from sqlalchemy.orm import relationship
from .base import Base


class UserDevice(Base):
    __tablename__ = "user_device"

    id = Column(BigInteger, primary_key=True, index=True)

    user_id = Column(
        BigInteger,
        ForeignKey("app_user.id", ondelete="CASCADE"),
        nullable=False
    )

    device_id = Column(String(255), nullable=True)
    platform = Column(String(30), nullable=True)

    fcm_token = Column(Text, unique=True, nullable=False)

    last_seen_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    is_active = Column(Boolean, nullable=False, server_default="true")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)