from pydantic import BaseModel
from datetime import date, datetime
from typing import List
from .purchase_order_line_item import PurchaseOrderLineItem, PurchaseOrderLineItemCreate

class PurchaseOrderBase(BaseModel):
    supplier_id: int
    order_date: date
    expected_date: date
    status: str = "DRAFT"

class PurchaseOrderCreate(PurchaseOrderBase):
    line_items: List[PurchaseOrderLineItemCreate]

class PurchaseOrderUpdate(BaseModel):
    supplier_id: int | None = None
    order_date: date | None = None
    expected_date: date | None = None
    status: str | None = None

class PurchaseOrder(PurchaseOrderBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    line_items: List[PurchaseOrderLineItem] = []

    class Config:
        from_attributes = True
