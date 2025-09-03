from fastapi import APIRouter, Depends
from app.core.config import settings
from app.schemas.user import User
from app.api.deps import get_current_active_admin_user

# mypy: disable-error-code=no-untyped-def

router = APIRouter()

@router.get("/")
def read_settings(current_user: User = Depends(get_current_active_admin_user)):
    """
    Retrieve settings.
    """
    return {
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "api_version": settings.API_VERSION,
    }
