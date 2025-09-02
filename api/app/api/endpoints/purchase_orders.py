from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_current_active_user, get_current_active_manager_user
from app.deps import get_db
from app.schemas.purchase_order_line_item import PurchaseOrderLineItemReceive

router = APIRouter()

@router.post("/", response_model=schemas.PurchaseOrder)
def create_purchase_order(
    *,
    db: Session = Depends(get_db),
    po_in: schemas.PurchaseOrderCreate,
    current_user: models.User = Depends(get_current_active_manager_user),
):
    """
    Create new purchase order.
    """
    po = crud.create_purchase_order(db=db, po_in=po_in)
    return po

@router.get("/", response_model=List[schemas.PurchaseOrder])
def read_purchase_orders(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Retrieve purchase orders.
    """
    pos = crud.get_purchase_orders(db, skip=skip, limit=limit)
    return pos

@router.get("/{po_id}", response_model=schemas.PurchaseOrder)
def read_purchase_order(
    *,
    db: Session = Depends(get_db),
    po_id: int,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Get purchase order by ID.
    """
    po = crud.get_purchase_order(db=db, po_id=po_id)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return po

@router.put("/{po_id}", response_model=schemas.PurchaseOrder)
def update_purchase_order(
    *,
    db: Session = Depends(get_db),
    po_id: int,
    po_in: schemas.PurchaseOrderUpdate,
    current_user: models.User = Depends(get_current_active_manager_user),
):
    """
    Update a purchase order.
    """
    po = crud.get_purchase_order(db=db, po_id=po_id)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    po = crud.update_purchase_order(db=db, po_id=po_id, po_in=po_in)
    return po

@router.post("/{po_id}/receive", response_model=schemas.PurchaseOrder)
def receive_purchase_order(
    *,
    db: Session = Depends(get_db),
    po_id: int,
    received_items: List[PurchaseOrderLineItemReceive],
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Receive items for a purchase order.
    """
    po = crud.receive_purchase_order(
        db=db, po_id=po_id, received_items=received_items, user_id=current_user.id
    )
    if not po:
        raise HTTPException(status_code=404, detail="Purchase Order not found")
    return po