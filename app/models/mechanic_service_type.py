from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


from .base import Base



class MechanicServiceType(Base):
    __tablename__ = "mechanic_service_type"

    mechanic_id = Column(
        BigInteger, 
        ForeignKey("mechanic_profile.id", ondelete="CASCADE"), 
        primary_key=True, 
        nullable=False
    )
    service_type_id = Column(
        BigInteger, 
        ForeignKey("service_type.id", ondelete="CASCADE"), 
        primary_key=True, 
        nullable=False
    )

    def __repr__(self):
        return f"<MechanicServiceType(mechanic_id={self.mechanic_id}, service_type_id={self.service_type_id})>"