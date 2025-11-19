from sqlalchemy import (
    Column, BigInteger, Numeric, String, CHAR, Enum, ForeignKey, DateTime, text
)
from sqlalchemy.orm import declarative_base, relationship
import enum
from datetime import datetime

from .base import Base

# Enums for payment_method and payment_status
class PaymentMethod(enum.Enum):
    CASH = "CASH"
    ONLINE = "ONLINE"

class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    SUCCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class Payment(Base):
    __tablename__ = 'payment'

    id = Column(BigInteger, primary_key=True)
    ticket_id = Column(BigInteger, ForeignKey('ticket.id', ondelete='RESTRICT'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(CHAR(3), nullable=False, default='NPR')
    method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    provider = Column(String(50))
    provider_reference = Column(String(100))
    paid_at = Column(
        DateTime(timezone=True))
    created_at = Column(
        DateTime(timezone=True), server_default=text("NOW()")
    )
