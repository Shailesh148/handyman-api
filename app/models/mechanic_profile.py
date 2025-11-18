from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    DECIMAL,
    ForeignKey,
    String,
    text,
    Integer
)
from sqlalchemy.orm import relationship

from .base import Base
import enum


class MechanicProfile(Base):
    __tablename__ = "mechanic_profile"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("app_user.id"), unique=True, nullable=False)
    base_location_id = Column(BigInteger, ForeignKey("location.id"), nullable=True)
    base_latitude = Column(DECIMAL(9, 6), nullable=True)
    base_longitude = Column(DECIMAL(9, 6), nullable=True)
    service_radius_km = Column(DECIMAL(9, 6), default=5.0)
    is_available = Column(Boolean, default=True, nullable=False)
    rating = Column(DECIMAL(9, 6), nullable=True)
    total_jobs_completed = Column(Integer, default=0, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=text("NOW()")
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=text("NOW()")
    )