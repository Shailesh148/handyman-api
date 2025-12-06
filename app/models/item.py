import enum
from sqlalchemy import (
	BigInteger,
	Column,
	Enum,
	String,
)
from .base import Base
from sqlalchemy.orm import relationship


class ItemType(str, enum.Enum):
	TOOL = "TOOL"
	PART = "PART"


class Item(Base):
	__tablename__ = "items"

	id = Column(BigInteger, primary_key=True, index=True)
	name = Column(String(150), nullable=False)
	item_type = Column(Enum(ItemType, name="item_type"), nullable=False)
	unit = Column(String(50), nullable=True)

	inventory = relationship("Inventory", back_populates="item")
