import enum
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    String,
    text,
)
from .base import Base
from sqlalchemy.orm import relationship


class UserRole(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    MECHANIC = "MECHANIC"
    OPERATOR = "OPERATOR"
    ADMIN = "ADMIN"


class AppUser(Base):
    __tablename__ = "app_user"

    id = Column(BigInteger, primary_key=True, index=True)
    auth0_user_id = Column(String(128), unique=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(255))
    role = Column(
        Enum(UserRole, name="user_role"),  # use existing enum
        nullable=False,
        server_default="CUSTOMER",
    )
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(
        DateTime(timezone=True), server_default=text("NOW()")
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=text("NOW()")
    )
    app_user_tickets = relationship("Ticket", back_populates= "customer")