from pydantic import BaseModel
from datetime import datetime

class InventoryTransactionBase(BaseModel):
    type: str
    quantity_change: int
    notes: str | None = None

class InventoryTransactionCreate(InventoryTransactionBase):
    item_id: int
    user_id: int
    new_quantity: int

class InventoryTransaction(InventoryTransactionBase):
    id: int
    item_id: int
    user_id: int
    new_quantity: int
    created_at: datetime

    class Config:
        from_attributes = True

class StockAdjustment(BaseModel):
    quantity_change: int
    notes: str | None = None
