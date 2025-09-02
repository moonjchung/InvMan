from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_inventory_value: float
    low_stock_items_count: int
    open_purchase_orders_count: int
    open_sales_orders_count: int
