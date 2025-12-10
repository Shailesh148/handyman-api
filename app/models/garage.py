import enum
from sqlalchemy import (
	BigInteger,
	Column,
	DateTime,
	String,
	text,
	ForeignKey,
	UniqueConstraint
)
from sqlalchemy.orm import relationship
from .base import Base


class Garage(Base):
	__tablename__ = "garages"

	id = Column(BigInteger, primary_key=True, index=True)
	name = Column(String(200), nullable=False)
	phone = Column(String(20), nullable=True)
	email = Column(String(255), nullable=True)
	address = Column(String, nullable=True)
	latitude = Column(String(50), nullable=True)
	longitude = Column(String(50), nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
	type = Column(String(100))
 
	staff = relationship("GarageUser", back_populates="garage", cascade="all, delete-orphan")
	inventory = relationship("Inventory", back_populates="garage")

class GarageUser(Base):
	__tablename__ = "garage_users"
	__table_args__ = (
		UniqueConstraint("garage_id", "user_id", name="uix_garage_user"),
	)

	id = Column(BigInteger, primary_key=True, index=True)
	garage_id = Column(BigInteger, ForeignKey("garages.id"), nullable=False)
	user_id = Column(BigInteger, ForeignKey("app_user.id"), nullable=False)
	role = Column(String(50), nullable=True)

	garage = relationship("Garage", back_populates="staff")
	customer = relationship("AppUser", back_populates="garage_users")
