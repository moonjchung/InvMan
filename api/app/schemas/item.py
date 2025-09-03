from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    sku: str
    name: str
    description: str | None = None
    price: float | None = Field(None, ge=0)
    average_cost: float | None = Field(0.0, ge=0)
    stock_level: int | None = Field(0, ge=0)
    unit: str | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    reorder_point: int | None = Field(None, ge=0)
    is_active: bool = True

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    sku: str | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    average_cost: float | None = None
    stock_level: int | None = None
    unit: str | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    reorder_point: int | None = None
    is_active: bool | None = None

class ItemInDBBase(ItemBase):
    id: int

    class Config:
        from_attributes = True

class Item(ItemInDBBase):
    pass
