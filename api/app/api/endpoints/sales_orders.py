from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_current_active_user, get_current_active_manager_user
from app.deps import get_db

# mypy: disable-error-code=no-untyped-def

router = APIRouter()

@router.post("/", response_model=schemas.SalesOrder)
def create_sales_order(
    *,
    db: Session = Depends(get_db),
    so_in: schemas.SalesOrderCreate,
    current_user: models.User = Depends(get_current_active_manager_user),
):
    """
    Create new sales order.
    """
    so = crud.create_sales_order(db=db, so_in=so_in)
    if not so:
        raise HTTPException(status_code=400, detail="Insufficient stock.")
    return so

@router.get("/", response_model=List[schemas.SalesOrder])
def read_sales_orders(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Retrieve sales orders.
    """
    sos = crud.get_sales_orders(db, skip=skip, limit=limit)
    return sos

@router.get("/{so_id}", response_model=schemas.SalesOrder)
def read_sales_order(
    *,
    db: Session = Depends(get_db),
    so_id: int,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Get sales order by ID.
    """
    so = crud.get_sales_order(db=db, so_id=so_id)
    if not so:
        raise HTTPException(status_code=404, detail="Sales Order not found")
    return so

@router.post("/{so_id}/fulfill", response_model=schemas.SalesOrder)
def fulfill_sales_order(
    *,
    db: Session = Depends(get_db),
    so_id: int,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Fulfill a sales order.
    """
    so = crud.fulfill_sales_order(db=db, so_id=so_id, user_id=current_user.id)
    if not so:
        raise HTTPException(status_code=400, detail="Could not fulfill order.")
    return so
