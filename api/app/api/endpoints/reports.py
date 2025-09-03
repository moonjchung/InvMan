from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_current_active_user
from app.deps import get_db
from app.schemas.report import ValuationReportItem

# mypy: disable-error-code=no-untyped-def

router = APIRouter()

@router.get("/valuation", response_model=List[ValuationReportItem])
def get_valuation_report(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    """
    Retrieve inventory valuation report.
    """
    items = crud.get_valuation_report(db)
    report = []
    for item in items:
        total_value = (item.stock_level or 0) * (item.average_cost or 0.0)
        report.append(
            ValuationReportItem(
                item_id=item.id,
                sku=item.sku,
                name=item.name,
                stock_level=item.stock_level,
                average_cost=item.average_cost,
                total_value=total_value,
            )
        )
    return report
