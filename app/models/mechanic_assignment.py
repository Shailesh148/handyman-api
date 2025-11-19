from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    DECIMAL,
    ForeignKey,
    String,
    text,
    Integer,
    UniqueConstraint,
    Enum
)
import enum



from sqlalchemy.orm import relationship


from .base import Base

class AssignmentStatus(str, enum.Enum):
    ASSIGNED = "ASSIGNED"
    VIEWED = "VIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class MechanicAssignmentModel(Base):
    __tablename__ = "mechanic_assignment"
    __table_args__ = (
        UniqueConstraint("ticket_id", "mechanic_id", name="uix_ticket_mechanic"),
    )
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ticket_id = Column(BigInteger, ForeignKey("ticket.id", ondelete="CASCADE"), nullable=False)
    mechanic_id = Column(BigInteger, ForeignKey("app_user.id"), nullable=False)
    status = Column(Enum(AssignmentStatus, name= "assignment_status"), nullable=False, server_default="ASSIGNED")
    distance_km = Column(DECIMAL(9, 6), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=text("NOW()")
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=text("NOW()")
    )
    
    ticket = relationship("Ticket", back_populates="assignments")