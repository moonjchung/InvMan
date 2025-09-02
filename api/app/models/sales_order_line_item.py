from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class SalesOrderLineItem(Base):
    __tablename__ = "sales_order_line_items"

    id = Column(Integer, primary_key=True, index=True)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity_ordered = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    sales_order = relationship("SalesOrder", back_populates="line_items")
    item = relationship("Item")
