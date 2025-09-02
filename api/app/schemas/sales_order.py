from pydantic import BaseModel
from datetime import date, datetime
from typing import List
from .sales_order_line_item import SalesOrderLineItem, SalesOrderLineItemCreate

class SalesOrderBase(BaseModel):
    customer_name: str
    order_date: date
    status: str = "DRAFT"

class SalesOrderCreate(SalesOrderBase):
    line_items: List[SalesOrderLineItemCreate]

class SalesOrderUpdate(BaseModel):
    customer_name: str | None = None
    order_date: date | None = None
    status: str | None = None

class SalesOrder(SalesOrderBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    line_items: List[SalesOrderLineItem] = []

    class Config:
        from_attributes = True
