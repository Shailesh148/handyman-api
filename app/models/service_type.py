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


class ServiceType(Base):
    __tablename__ = "service_type"

    id = Column(BigInteger, primary_key=True, index=True)
    category_id = Column(BigInteger, ForeignKey("service_category.id"), nullable=True)

    name = Column(String(100))
    description = Column(Text)
