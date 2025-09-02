import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session

# Load .env before app modules
from dotenv import load_dotenv
load_dotenv()

from app import crud, schemas, models
from app.db.session import SessionLocal
from app.core.config import settings
from alembic.config import Config
from alembic import command


fake = Faker()

def seed_data():
    db = SessionLocal()
    try:
        print("Upgrading database to latest version...")
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        command.upgrade(alembic_cfg, "head")
        print("Database upgrade complete.")

        print("Seeding data...")

        # 1. Create Users
        admin_user = crud.get_user_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
        if not admin_user:
            user_in = schemas.UserCreateByAdmin(email=settings.FIRST_SUPERUSER_EMAIL, password=settings.FIRST_SUPERUSER_PASSWORD, role="admin")
            crud.create_user_by_admin(db, user=user_in)
            print("Admin user created.")

        manager_user = crud.get_user_by_email(db, email="manager@example.com")
        if not manager_user:
            user_in = schemas.UserCreateByAdmin(email="manager@example.com", password="managerpassword", role="manager")
            crud.create_user_by_admin(db, user=user_in)
            print("Manager user created.")

        staff_user = crud.get_user_by_email(db, email="staff@example.com")
        if not staff_user:
            user_in = schemas.UserCreateByAdmin(email="staff@example.com", password="staffpassword", role="staff")
            crud.create_user_by_admin(db, user=user_in)
            print("Staff user created.")

        # 2. Create Suppliers
        suppliers = crud.get_suppliers(db, limit=10)
        if not suppliers:
            print("Creating suppliers...")
            for _ in range(10):
                supplier_in = schemas.SupplierCreate(name=fake.company())
                crud.create_supplier(db, supplier=supplier_in)
            suppliers = crud.get_suppliers(db, limit=10)

        # 3. Create Categories
        categories = crud.get_categories(db, limit=8)
        if not categories:
            print("Creating categories...")
            cat_names = ["Produce", "Bakery", "Dairy", "Meat", "Pantry", "Frozen", "Electronics", "Apparel"]
            for name in cat_names:
                cat_in = schemas.CategoryCreate(name=name)
                crud.create_category(db, category=cat_in)
            categories = crud.get_categories(db, limit=8)

        # 4. Create Items
        items = crud.get_items(db, limit=30)
        if not items:
            print("Creating items...")
            for i in range(30):
                name = fake.unique.word().capitalize()
                item_in = schemas.ItemCreate(
                    sku=f"TEST-SKU-{i:04d}",
                    name=f"{name} {fake.bs()}",
                    description=fake.sentence(),
                    price=round(random.uniform(1.5, 250.0), 2),
                    unit="piece",
                    stock_level=random.randint(0, 200),
                    reorder_point=random.randint(10, 30),
                    supplier_id=random.choice(suppliers).id,
                    category_id=random.choice(categories).id,
                )
                if i % 4 == 0: # Make some items low stock
                    item_in.stock_level = random.randint(0, item_in.reorder_point)
                crud.upsert_item(db, item_in=item_in)
            items = crud.get_items(db, limit=30)

        # 5. Create Purchase Orders
        purchase_orders = crud.get_purchase_orders(db, limit=5)
        if not purchase_orders:
            print("Creating purchase orders...")
            for _ in range(5):
                supplier = random.choice(suppliers)
                line_items_in = []
                for _ in range(random.randint(1, 5)):
                    item = random.choice(items)
                    line_items_in.append(schemas.PurchaseOrderLineItemCreate(
                        item_id=item.id,
                        quantity_ordered=random.randint(50, 100),
                        unit_cost=round(item.price * random.uniform(0.6, 0.8), 2)
                    ))
                po_in = schemas.PurchaseOrderCreate(
                    supplier_id=supplier.id, 
                    status="ORDERED", 
                    order_date=datetime.utcnow().date() - timedelta(days=random.randint(1, 10)),
                    expected_date=datetime.utcnow().date() + timedelta(days=random.randint(5, 20)),
                    line_items=line_items_in
                )
                crud.create_purchase_order(db, po_in=po_in)

        # 6. Create Sales Orders
        sales_orders = crud.get_sales_orders(db, limit=5)
        if not sales_orders:
            print("Creating sales orders...")
            for _ in range(5):
                line_items_in = []
                for _ in range(random.randint(1, 3)):
                    item = random.choice(items)
                    if item.stock_level > 10: # Only sell items with enough stock
                        line_items_in.append(schemas.SalesOrderLineItemCreate(
                            item_id=item.id,
                            quantity_ordered=random.randint(1, 5),
                            unit_price=item.price
                        ))
                if line_items_in:
                    so_in = schemas.SalesOrderCreate(
                        customer_name=fake.name(), 
                        status="CONFIRMED", 
                        order_date=datetime.utcnow().date() - timedelta(days=random.randint(1, 20)),
                        line_items=line_items_in
                    )
                    crud.create_sales_order(db, so_in=so_in)

        print("Seeding finished successfully.")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
