import os

# Set required environment variables before importing app modules
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "secret")
os.environ.setdefault("FIRST_SUPERUSER_EMAIL", "super@example.com")
os.environ.setdefault("FIRST_SUPERUSER_PASSWORD", "password")
os.environ.setdefault("FIRST_MANAGER_EMAIL", "manager@example.com")
os.environ.setdefault("FIRST_MANAGER_PASSWORD", "password")
os.environ.setdefault("FIRST_STAFF_EMAIL", "staff@example.com")
os.environ.setdefault("FIRST_STAFF_PASSWORD", "password")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app import models, crud
from app.schemas.purchase_order_line_item import PurchaseOrderLineItemReceive

def _init_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()

def test_receive_purchase_order_caps_quantity():
    db = _init_db()

    supplier = models.Supplier(name="Supplier1")
    user = models.User(email="user@example.com", hashed_password="hashed")
    item = models.Item(sku="SKU1", name="Item1", stock_level=0, average_cost=0.0, supplier=supplier)
    po = models.PurchaseOrder(supplier=supplier, status="PENDING")
    line_item = models.PurchaseOrderLineItem(
        purchase_order=po,
        item=item,
        quantity_ordered=10,
        quantity_received=0,
        unit_cost=2.0,
    )

    db.add_all([supplier, user, item, po, line_item])
    db.commit()
    db.refresh(line_item)
    db.refresh(item)

    received = PurchaseOrderLineItemReceive(id=line_item.id, quantity=15)
    crud.receive_purchase_order(db, po.id, [received], user_id=user.id)

    db.refresh(line_item)
    db.refresh(item)

    assert line_item.quantity_received == 10
    assert item.stock_level == 10

    transactions = db.query(models.InventoryTransaction).filter_by(item_id=item.id).all()
    assert len(transactions) == 1
    assert transactions[0].quantity_change == 10
