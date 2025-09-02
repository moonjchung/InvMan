from pydantic import BaseModel

class PurchaseOrderLineItemBase(BaseModel):
    item_id: int
    quantity_ordered: int
    unit_cost: float

class PurchaseOrderLineItemCreate(PurchaseOrderLineItemBase):
    pass

class PurchaseOrderLineItem(PurchaseOrderLineItemBase):
    id: int
    quantity_received: int

    class Config:
        from_attributes = True

class PurchaseOrderLineItemReceive(BaseModel):
    id: int
    quantity: int