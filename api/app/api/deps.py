from fastapi import Depends, HTTPException, status, Request
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core.config import settings
from app.deps import get_db

def get_token_from_cookie(request: Request) -> str | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
    # The token is in the format "Bearer <token>"
    parts = token.split()
    if len(parts) == 2 and parts[0] == "Bearer":
        return parts[1]
    return None

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(get_token_from_cookie)
) -> models.User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.get_user_by_email(db, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_admin_user(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user

def get_current_active_manager_user(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
