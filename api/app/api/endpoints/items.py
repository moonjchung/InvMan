import csv
import io

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from typing import Any, Iterator, cast

from app import crud, models, schemas
from app.api.deps import get_current_active_user, get_current_active_manager_user
from app.deps import get_db
from app.schemas.inventory_transaction import StockAdjustment
from app.services import pdf

router = APIRouter()


@router.post("/import/csv")
def import_csv(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_active_manager_user),
) -> dict[str, str]:
    """
    Import items from CSV.
    """
    try:
        contents = file.file.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(contents))
        for row in reader:
            item_in = schemas.ItemCreate(**cast(dict[str, Any], row))
            crud.upsert_item(db, item_in=item_in)
    except Exception:
        # TODO: Add logging
        raise HTTPException(
            status_code=400,
            detail="Error processing CSV file. Please check the file format.",
        )

    return {"message": "CSV imported successfully"}


@router.get("/export/csv")
def export_csv(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_manager_user),
) -> StreamingResponse:
    """
    Export items to CSV.
    """
    def iter_items() -> Iterator[str]:
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(["id", "sku", "name", "description", "price", "stock_level", "unit", "category_id", "supplier_id", "reorder_point", "is_active"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        items_generator = crud.get_items_generator(db)
        for item in items_generator:
            writer.writerow([item.id, item.sku, item.name, item.description, item.price, item.stock_level, item.unit, item.category_id, item.supplier_id, item.reorder_point, item.is_active])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    return StreamingResponse(iter_items(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=items.csv"})


@router.get("/", response_model=list[schemas.Item])
def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
) -> list[models.Item]:
    """
    Retrieve items.
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: schemas.ItemCreate,
    current_user: models.User = Depends(get_current_active_manager_user),
) -> models.Item:
    """
    Create new item.
    """
    item = crud.create_item(db=db, item=item_in)
    return item


@router.get("/sku/{sku}", response_model=schemas.Item)
def read_item_by_sku(
    *,
    db: Session = Depends(get_db),
    sku: str,
    current_user: models.User = Depends(get_current_active_user),
) -> models.Item:
    """
    Get item by SKU.
    """
    item = crud.get_item_by_sku(db=db, sku=sku)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/{item_id}", response_model=schemas.Item)
def read_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: models.User = Depends(get_current_active_user),
) -> models.Item:
    """
    Get item by ID.
    """
    item = crud.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    item_in: schemas.ItemUpdate,
    current_user: models.User = Depends(get_current_active_manager_user),
) -> models.Item:
    """
    Update an item.
    """
    item = crud.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.update_item(db=db, item_id=item_id, item=item_in)
    assert item is not None
    return item


@router.delete("/{item_id}", response_model=schemas.Item)
def delete_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: models.User = Depends(get_current_active_manager_user),
) -> models.Item:
    """
    Delete an item.
    """
    item = crud.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.delete_item(db=db, item_id=item_id)
    assert item is not None
    return item


@router.post("/{item_id}/adjust", response_model=schemas.Item)
def adjust_stock(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    adjustment_in: StockAdjustment,
    current_user: models.User = Depends(get_current_active_manager_user),
) -> models.Item:
    """
    Adjust stock for an item.
    """
    item = crud.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = crud.adjust_stock(
        db=db, item_id=item_id, adjustment=adjustment_in, user_id=current_user.id
    )
    if updated_item is None:
        raise HTTPException(status_code=400, detail="Stock level cannot be negative.")
    return updated_item


@router.get("/{item_id}/label.pdf", response_class=StreamingResponse)
def get_item_label(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: models.User = Depends(get_current_active_user),
) -> StreamingResponse:
    """
    Generate and return a PDF label for an item.
    """
    item = crud.get_item(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
        pdf_buffer = pdf.generate_item_label(item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    headers = {
        'Content-Disposition': f'inline; filename="{item.sku}_label.pdf"'
    }
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)
