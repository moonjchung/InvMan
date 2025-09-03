from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:  # pragma: no cover
    from .item import Item
    from .sales_order import SalesOrder

from app.db.base import Base


class SalesOrderLineItem(Base):
    __tablename__ = "sales_order_line_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    sales_order_id: Mapped[int] = mapped_column(
        ForeignKey("sales_orders.id"), nullable=False
    )
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    quantity_ordered: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)

    sales_order: Mapped["SalesOrder"] = relationship(
        "SalesOrder", back_populates="line_items"
    )
    item: Mapped["Item"] = relationship("Item")
