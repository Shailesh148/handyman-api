import enum
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    text,
)
from .base import Base


class TicketStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    DISPATCH_PENDING = "DISPATCH_PENDING"
    ASSIGNED = "ASSIGNED"
    ACCEPTED = "ACCEPTED"
    ON_THE_WAY = "ON_THE_WAY"
    ESTIMATE_PROVIDED = "ESTIMATE_PROVIDED"
    ESTIMATE_APPROVED = "ESTIMATE_APPROVED"
    ESTIMATE_REJECTED = "ESTIMATE_REJECTED"
    WORK_STARTED = "WORK_STARTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(BigInteger, primary_key=True, index=True)
    ticket_code = Column(String(30), unique=True, nullable=False)

    customer_id = Column(
        BigInteger, ForeignKey("app_user.id"), nullable=False
    )
    service_issue_id = Column(
        BigInteger, ForeignKey("service_issue.id"), nullable=False
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
