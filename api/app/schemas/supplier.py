from pydantic import BaseModel

class SupplierBase(BaseModel):
    name: str

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: str | None = None

class Supplier(SupplierBase):
    id: int

    class Config:
        from_attributes = True