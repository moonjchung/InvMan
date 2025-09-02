from sqlalchemy import Column, Integer, String, DateTime, func, Date
from sqlalchemy.orm import relationship
from app.db.base import Base

class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    status = Column(String, nullable=False, default="DRAFT")
    order_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    line_items = relationship("SalesOrderLineItem", back_populates="sales_order")
