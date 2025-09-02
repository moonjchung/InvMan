from pydantic import BaseModel

class SalesOrderLineItemBase(BaseModel):
    item_id: int
    quantity_ordered: int
    unit_price: float

class SalesOrderLineItemCreate(SalesOrderLineItemBase):
    pass

class SalesOrderLineItem(SalesOrderLineItemBase):
    id: int

    class Config:
        from_attributes = True
