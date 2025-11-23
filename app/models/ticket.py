import enum
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    text,Enum, CHAR, Numeric
)
from sqlalchemy import Column, BigInteger, String, SmallInteger, Boolean, ForeignKey, Enum, TIMESTAMP, func
from .base import Base

from sqlalchemy.orm import relationship

class TicketStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    DISPATCH_PENDING = "DISPATCH_PENDING"
    ASSIGNED = "ASSIGNED"
    ACCEPTED = "ACCEPTED"
    ON_THE_WAY = "ON_THE_WAY"
    ESTIMATE_APPROVED_DELETED = "ESTIMATE_APPROVED"
    ESTIMATE_REJECTED_DELETED = "ESTIMATE_REJECTED"
    ESTIMATE_PROVIDED = "ESTIMATE_PROVIDED"
    ESTIMATE_APPROVED = "WORK_IN_PROGRESS"
    ESTIMATE_REJECTED = "REJECTED"
    WORK_STARTED = "WORK_STARTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


ESTIMATE_TO_TICKET_STATUS = {
    "PENDING_CUSTOMER_APPROVAL": TicketStatus.ESTIMATE_PROVIDED,
    "APPROVED": TicketStatus.ESTIMATE_APPROVED,
    "REJECTED": TicketStatus.ESTIMATE_REJECTED
}

class Vehicle(Base):
    __tablename__ = "vehicle"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("app_user.id"), nullable=False)
    type = Column(String(100))
    brand = Column(String(100))
    model = Column(String(100))
    year = Column(SmallInteger)
    license_plate = Column(String(50))
    is_default = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)




class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(BigInteger, primary_key=True, index=True)
    ticket_code = Column(String(30), unique=True, nullable=False)

    customer_id = Column(
        BigInteger, ForeignKey("app_user.id"), nullable=False
    )
    service_type_id = Column(
        BigInteger, ForeignKey("service_type.id"), nullable=False
    )
    vehicle_id = Column(
        BigInteger, ForeignKey("vehicle.id"), nullable=True
    )
    customer_location_id = Column(
        BigInteger, ForeignKey("location.id"), nullable=True
    )

    status = Column(
        Enum(TicketStatus, name="ticket_status"),
        nullable=False,
        server_default="REQUESTED",
    )
    description = Column(Text)

    requested_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("NOW()")
    )
    scheduled_at = Column(DateTime(timezone=True), nullable=True)

    preferred_payment_method = Column(
        Enum("CASH", "ONLINE", "WALLET", name="payment_method"),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("NOW()")
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("NOW()")
    )
    
    assignments = relationship("MechanicAssignmentModel", back_populates="ticket")
    customer = relationship("AppUser", back_populates= "app_user_tickets")
    payments = relationship("Payment", back_populates="ticket")
    estimates = relationship("Estimate", back_populates="ticket")
    service_type = relationship("ServiceType", back_populates="ticket")