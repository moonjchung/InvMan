from pydantic import BaseModel, Field

class PurchaseOrderLineItemBase(BaseModel):
    item_id: int
    quantity_ordered: int = Field(..., gt=0)
    unit_cost: float = Field(..., ge=0)

class PurchaseOrderLineItemCreate(PurchaseOrderLineItemBase):
    pass

class PurchaseOrderLineItem(PurchaseOrderLineItemBase):
    id: int
    quantity_received: int

    class Config:
        from_attributes = True

class PurchaseOrderLineItemReceive(BaseModel):
    id: int
    quantity: int = Field(..., gt=0)