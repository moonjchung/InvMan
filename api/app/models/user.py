from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    role = Column(String, nullable=False, default='staff') # admin, manager, staff
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship("InventoryTransaction", back_populates="user")
