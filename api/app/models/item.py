from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:  # pragma: no cover
    from .category import Category
    from .supplier import Supplier
    from .inventory_transaction import InventoryTransaction
    from .sales_order_line_item import SalesOrderLineItem

from app.db.base import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sku: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[float | None] = mapped_column(Float, nullable=True)
    average_cost: Mapped[float] = mapped_column(Float, default=0.0)
    stock_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unit: Mapped[str | None] = mapped_column(String, nullable=True)

    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category" | None] = relationship("Category", back_populates="items")

    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("suppliers.id"))
    supplier: Mapped["Supplier" | None] = relationship("Supplier", back_populates="items")

    reorder_point: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    transactions: Mapped[list["InventoryTransaction"]] = relationship(
        "InventoryTransaction", back_populates="item"
    )
    sales_order_line_items: Mapped[list["SalesOrderLineItem"]] = relationship(
        "SalesOrderLineItem", back_populates="item"
    )