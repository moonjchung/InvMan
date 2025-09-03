from collections.abc import Generator
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.item import Item
from app.models.user import User
from app.models.category import Category
from app.models.supplier import Supplier
from app.models.inventory_transaction import InventoryTransaction
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_line_item import PurchaseOrderLineItem
from app.models.sales_order import SalesOrder
from app.models.sales_order_line_item import SalesOrderLineItem
from app.schemas.item import ItemCreate, ItemUpdate
from app.schemas.user import UserCreate, UserCreateByAdmin
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.supplier import SupplierCreate, SupplierUpdate
from app.schemas.inventory_transaction import StockAdjustment
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate
from app.schemas.purchase_order_line_item import PurchaseOrderLineItemReceive
from app.schemas.sales_order import SalesOrderCreate
from app.schemas.dashboard import DashboardSummary
from app.services.email import send_low_stock_alert
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_by_admin(db: Session, user: UserCreateByAdmin) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    if limit is None:
        return db.query(Item).offset(skip).all()
    return db.query(Item).offset(skip).limit(limit).all()


def get_items_generator(db: Session, chunk_size: int = 1000) -> Generator[Item, None, None]:
    offset = 0
    while True:
        items = db.query(Item).offset(offset).limit(chunk_size).all()
        if not items:
            break
        for item in items:
            yield item
        offset += chunk_size


def get_item_by_sku(db: Session, sku: str) -> Item | None:
    return db.query(Item).filter(Item.sku == sku).first()

def upsert_item(db: Session, item_in: ItemCreate) -> Item:
    db_item = get_item_by_sku(db, sku=item_in.sku)
    if db_item:
        update_data = item_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    else:
        return create_item(db, item=item_in)

def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int) -> Item | None:
    return db.query(Item).filter(Item.id == item_id).first()


def update_item(db: Session, item_id: int, item: ItemUpdate) -> Item | None:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        update_data = item.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> Item | None:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


def adjust_stock(
    db: Session, item_id: int, adjustment: StockAdjustment, user_id: int
) -> Item | None:
    """
    Adjust stock for an item. Creates an inventory transaction.
    This function is transactional.
    """
    db_item = db.query(Item).filter(Item.id == item_id).with_for_update().first()
    if not db_item:
        return None

    new_stock_level = db_item.stock_level + adjustment.quantity_change
    if new_stock_level < 0:
        return None # Indicate failure

    db_item.stock_level = new_stock_level

    transaction = InventoryTransaction(
        item_id=item_id,
        user_id=user_id,
        type="adjustment",
        quantity_change=adjustment.quantity_change,
        new_quantity=new_stock_level,
        notes=adjustment.notes,
    )
    db.add(transaction)
    db.commit()
    db.refresh(db_item)

    if db_item.reorder_point is not None and new_stock_level <= db_item.reorder_point:
        send_low_stock_alert(db_item.name, db_item.sku, new_stock_level)

    return db_item

def get_purchase_order(db: Session, po_id: int) -> PurchaseOrder | None:
    return db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()

def get_purchase_orders(db: Session, skip: int = 0, limit: int = 100) -> List[PurchaseOrder]:
    return db.query(PurchaseOrder).offset(skip).limit(limit).all()

def create_purchase_order(db: Session, po_in: PurchaseOrderCreate) -> PurchaseOrder:
    po_data = po_in.dict(exclude={"line_items"})
    db_po = PurchaseOrder(**po_data)
    db.add(db_po)
    db.flush()

    for line_item_in in po_in.line_items:
        db_line_item = PurchaseOrderLineItem(
            **line_item_in.dict(), purchase_order_id=db_po.id
        )
        db.add(db_line_item)
    db.commit()
    db.refresh(db_po)
    return db_po

def update_purchase_order(db: Session, po_id: int, po_in: PurchaseOrderUpdate) -> PurchaseOrder | None:
    db_po = get_purchase_order(db, po_id)
    if not db_po:
        return None
    update_data = po_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_po, key, value)
    db.add(db_po)
    db.commit()
    db.refresh(db_po)
    return db_po

def receive_purchase_order(
    db: Session,
    po_id: int,
    received_items: List[PurchaseOrderLineItemReceive],
    user_id: int,
) -> PurchaseOrder | None:
    db_po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).with_for_update().first()
    if not db_po:
        return None

    for received_item in received_items:
        line_item = db.query(PurchaseOrderLineItem).filter(PurchaseOrderLineItem.id == received_item.id).with_for_update().first()
        if not line_item or line_item.purchase_order_id != po_id:
            # Or raise an exception
            continue

        item = (
            db.query(Item)
            .filter(Item.id == line_item.item_id)
            .with_for_update()
            .first()
        )

        remaining_qty = line_item.quantity_ordered - line_item.quantity_received
        received_qty = min(received_item.quantity, remaining_qty)
        if received_qty <= 0:
            continue

        # Calculate new average cost
        old_stock = item.stock_level
        old_avg_cost = item.average_cost if item.average_cost is not None else 0.0
        received_cost = (
            line_item.unit_cost if line_item.unit_cost is not None else 0.0
        )

        new_stock_level = old_stock + received_qty
        if new_stock_level > 0:
            new_avg_cost = (
                (old_stock * old_avg_cost) + (received_qty * received_cost)
            ) / new_stock_level
            item.average_cost = new_avg_cost
        elif received_qty > 0:
            item.average_cost = received_cost

        line_item.quantity_received += received_qty
        item.stock_level += received_qty

        transaction = InventoryTransaction(
            item_id=item.id,
            user_id=user_id,
            type="receipt",
            quantity_change=received_qty,
            new_quantity=item.stock_level,
            notes=f"PO #{db_po.id}",
        )
        db.add(transaction)

    # Check if PO is complete
    all_received = all(li.quantity_received >= li.quantity_ordered for li in db_po.line_items)
    if all_received:
        db_po.status = "COMPLETE"
    else:
        db_po.status = "PARTIALLY_RECEIVED"

    db.commit()
    db.refresh(db_po)
    return db_po

def get_valuation_report(db: Session) -> List[Item]:
    return db.query(Item).all()

def get_dashboard_summary(db: Session) -> DashboardSummary:
    total_inventory_value = db.query(func.sum(Item.stock_level * Item.average_cost)).scalar() or 0.0
    low_stock_items_count = db.query(Item).filter(Item.stock_level <= Item.reorder_point).count()
    open_purchase_orders_count = db.query(PurchaseOrder).filter(PurchaseOrder.status.notin_(['COMPLETE', 'CANCELLED'])).count()
    open_sales_orders_count = db.query(SalesOrder).filter(SalesOrder.status.notin_(['SHIPPED', 'CANCELLED'])).count()

    return DashboardSummary(
        total_inventory_value=total_inventory_value,
        low_stock_items_count=low_stock_items_count,
        open_purchase_orders_count=open_purchase_orders_count,
        open_sales_orders_count=open_sales_orders_count,
    )

def get_sales_order(db: Session, so_id: int) -> SalesOrder | None:
    return db.query(SalesOrder).filter(SalesOrder.id == so_id).first()

def get_sales_orders(db: Session, skip: int = 0, limit: int = 100) -> List[SalesOrder]:
    return db.query(SalesOrder).offset(skip).limit(limit).all()

def create_sales_order(db: Session, so_in: SalesOrderCreate) -> SalesOrder | None:
    # Check for sufficient stock
    for line_item_in in so_in.line_items:
        item = get_item(db, line_item_in.item_id)
        if not item or item.stock_level < line_item_in.quantity_ordered:
            return None # Insufficient stock

    so_data = so_in.dict(exclude={"line_items"})
    db_so = SalesOrder(**so_data)
    db.add(db_so)
    db.commit()
    db.refresh(db_so)

    for line_item_in in so_in.line_items:
        db_line_item = SalesOrderLineItem(
            **line_item_in.dict(), sales_order_id=db_so.id
        )
        db.add(db_line_item)
    db.commit()
    db.refresh(db_so)
    return db_so

def fulfill_sales_order(db: Session, so_id: int, user_id: int) -> SalesOrder | None:
    db_so = get_sales_order(db, so_id)
    if not db_so or db_so.status != "CONFIRMED":
        return None

    for li in db_so.line_items:
        item = db.query(Item).filter(Item.id == li.item_id).with_for_update().first()
        if item.stock_level < li.quantity_ordered:
            # This should not happen if we check on creation, but as a safeguard
            return None
        
        item.stock_level -= li.quantity_ordered
        transaction = InventoryTransaction(
            item_id=item.id,
            user_id=user_id,
            type="sale",
            quantity_change=-li.quantity_ordered,
            new_quantity=item.stock_level,
            notes=f"SO #{db_so.id}",
        )
        db.add(transaction)

    db_so.status = "SHIPPED"
    db.commit()
    db.refresh(db_so)
    return db_so

def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: CategoryCreate) -> Category:
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
    db: Session, category_id: int, category: CategoryUpdate
) -> Category | None:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        update_data = category.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int) -> Category | None:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category


def get_supplier(db: Session, supplier_id: int) -> Supplier | None:
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()


def get_suppliers(db: Session, skip: int = 0, limit: int = 100) -> List[Supplier]:
    return db.query(Supplier).offset(skip).limit(limit).all()


def create_supplier(db: Session, supplier: SupplierCreate) -> Supplier:
    db_supplier = Supplier(name=supplier.name)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def update_supplier(
    db: Session, supplier_id: int, supplier: SupplierUpdate
) -> Supplier | None:
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if db_supplier:
        update_data = supplier.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_supplier, key, value)
        db.commit()
        db.refresh(db_supplier)
    return db_supplier


def delete_supplier(db: Session, supplier_id: int) -> Supplier | None:
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if db_supplier:
        db.delete(db_supplier)
        db.commit()
    return db_supplier

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def is_active(user: User) -> bool:
    return user.is_active
