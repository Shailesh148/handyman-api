from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    DECIMAL,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .base import Base


class ServiceIssue(Base):
    __tablename__ = "service_issue"

    id = Column(BigInteger, primary_key=True, index=True)
    service_type_id = Column(BigInteger, ForeignKey("service_type.id"), nullable=True)

    name = Column(String(100))
    description = Column(Text)