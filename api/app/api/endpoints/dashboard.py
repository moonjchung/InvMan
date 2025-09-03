from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models
from app.api.deps import get_current_active_user
from app.deps import get_db
from app.schemas.dashboard import DashboardSummary

router = APIRouter()

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
) -> DashboardSummary:
    """
    Retrieve dashboard summary.
    """
    return crud.get_dashboard_summary(db)
