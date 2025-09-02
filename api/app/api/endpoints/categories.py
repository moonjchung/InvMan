from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_current_active_user, get_current_active_manager_user
from app.deps import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Retrieve categories.
    """
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@router.post("/", response_model=schemas.Category)
def create_category(
    *,
    db: Session = Depends(get_db),
    category_in: schemas.CategoryCreate,
    current_user: models.User = Depends(get_current_active_manager_user),
):
    """
    Create new category.
    """
    category = crud.create_category(db=db, category=category_in)
    return category


@router.get("/{category_id}", response_model=schemas.Category)
def read_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    current_user: models.User = Depends(get_current_active_user),
):
    """
    Get category by ID.
    """
    category = crud.get_category(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    category_in: schemas.CategoryUpdate,
    current_user: models.User = Depends(get_current_active_manager_user),
):
    """
    Update a category.
    """
    category = crud.get_category(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.update_category(db=db, category_id=category_id, category=category_in)
    return category


@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    current_user: models.User = Depends(get_current_active_manager_user),
):
    """
    Delete a category.
    """
    category = crud.get_category(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.delete_category(db=db, category_id=category_id)
    return category
