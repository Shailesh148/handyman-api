from sqlalchemy import (
    Column, BigInteger, Numeric, String, Text, ForeignKey, Enum, CHAR, DateTime, func
)
from sqlalchemy.orm import relationship, declarative_base
import enum

from .base import Base

# Define the Enum in Python to match your PostgreSQL enum
class EstimateStatusEnum(enum.Enum):
    PENDING_CUSTOMER_APPROVAL = "PENDING_CUSTOMER_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    # Add other statuses if needed

class Estimate(Base):
    __tablename__ = "estimate"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ticket_id = Column(BigInteger, ForeignKey("ticket.id", ondelete="CASCADE"), unique=True, nullable=False)
    mechanic_id = Column(BigInteger, ForeignKey("app_user.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(CHAR(3), nullable=False, default="NPR")
    status = Column(Enum(EstimateStatusEnum), nullable=False, default=EstimateStatusEnum.PENDING_CUSTOMER_APPROVAL)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    approved_at = Column(DateTime(timezone=True))
    rejected_at = Column(DateTime(timezone=True))