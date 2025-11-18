from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    DECIMAL,
    ForeignKey,
    String,
    text,
)
from sqlalchemy.orm import relationship

from .base import Base


class Location(Base):
    __tablename__ = "location"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("app_user.id"), nullable=True)

    label = Column(String(100))
    address_line1 = Column(String(255))
    address_line2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    latitude = Column(DECIMAL(9, 6))
    longitude = Column(DECIMAL(9, 6))
    is_primary = Column(Boolean, nullable=False, server_default="false")

    created_at = Column(
        DateTime(timezone=True), server_default=text("NOW()")
    )

    # optional relationship back to user
    user = relationship("AppUser", backref="locations")
