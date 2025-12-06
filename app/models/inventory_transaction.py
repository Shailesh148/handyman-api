import enum
from sqlalchemy import (
	BigInteger,
	Column,
	DateTime,
	Enum,
	ForeignKey,
	Integer,
	text,
)
from .base import Base


class InventoryTransactionType(str, enum.Enum):
	USED_ON_JOB = "USED_ON_JOB"
	RETURNED = "RETURNED"
	PURCHASED = "PURCHASED"
	DAMAGED = "DAMAGED"


class InventoryTransaction(Base):
	__tablename__ = "inventory_transactions"

	id = Column(BigInteger, primary_key=True, index=True)
	item_id = Column(BigInteger, ForeignKey("items.id"), nullable=False)
	garage_id = Column(BigInteger, ForeignKey("garages.id"), nullable=True)
	operator_user_id = Column(BigInteger, ForeignKey("app_user.id"), nullable=True)
	quantity_change = Column(Integer, nullable=False)
	transaction_type = Column(Enum(InventoryTransactionType, name="inventory_transaction_type"), nullable=False)
	reference_ticket_id = Column(BigInteger, ForeignKey("ticket.id"), nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))

