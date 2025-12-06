from sqlalchemy import (
	BigInteger,
	Column,
	DateTime,
	ForeignKey,
	Integer,
	text,
	CheckConstraint,
)
from sqlalchemy.orm import relationship
from .base import Base


class Inventory(Base):
	__tablename__ = "inventory"
	__table_args__ = (
		CheckConstraint(
			"(garage_id IS NOT NULL AND operator_user_id IS NULL) OR (garage_id IS NULL AND operator_user_id IS NOT NULL)",
			name="chk_inventory_owner",
		),
	)

	id = Column(BigInteger, primary_key=True, index=True)
	item_id = Column(BigInteger, ForeignKey("items.id"), nullable=False)
	garage_id = Column(BigInteger, ForeignKey("garages.id"), nullable=True)
	operator_user_id = Column(BigInteger, ForeignKey("app_user.id"), nullable=True)
	quantity = Column(Integer, nullable=False, server_default="0")
	minimum_quantity = Column(Integer, nullable=False, server_default="0")
	maximum_quantity = Column(Integer, nullable=False, server_default="0")
	updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
	garage = relationship("Garage", back_populates="inventory")

	item = relationship("Item", back_populates="inventory")

