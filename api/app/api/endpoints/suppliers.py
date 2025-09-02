from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_current_active_user, get_current_active_manager_user
from app.deps import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Supplier])
def read_suppliers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Retrieve suppliers.
    """
    suppliers = crud.get_suppliers(db, skip=skip, limit=limit)
    return suppliers


@router.post("/", response_model=schemas.Supplier)
def create_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_in: schemas.SupplierCreate,
    current_user: models.User = Depends(get_current_active_manager_user),
):
    """
    Create new supplier.
    """
    supplier = crud.create_supplier(db=db, supplier=supplier_in)
    return supplier


@router.get("/{supplier_id}", response_model=schemas.Supplier)
def read_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_id: int,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Get supplier by ID.
    """
    supplier = crud.get_supplier(db=db, supplier_id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.put("/{supplier_id}", response_model=schemas.Supplier)
def update_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_id: int,
    supplier_in: schemas.SupplierUpdate,
    current_user: models.User = Depends(get_current_active_manager_user),
):
    """
    Update a supplier.
    """
    supplier = crud.get_supplier(db=db, supplier_id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier = crud.update_supplier(db=db, supplier_id=supplier_id, supplier=supplier_in)
    return supplier


@router.delete("/{supplier_id}", response_model=schemas.Supplier)
def delete_supplier(
    *,
    db: Session = Depends(get_db),
    supplier_id: int,
    current_user: models.User = Depends(get_current_active_manager_user),
):
    """
    Delete a supplier.
    """
    supplier = crud.get_supplier(db=db, supplier_id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier = crud.delete_supplier(db=db, supplier_id=supplier_id)
    return supplier
