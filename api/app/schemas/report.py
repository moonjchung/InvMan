from pydantic import BaseModel

class ValuationReportItem(BaseModel):
    item_id: int
    sku: str
    name: str
    stock_level: int
    average_cost: float
    total_value: float

    class Config:
        from_attributes = True
