
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.core.security import create_access_token
from app.deps import get_db

router = APIRouter()


class LoginRequest(BaseModel):
    """Schema for login requests."""

    email: str
    password: str


@router.post("/login")
async def login_for_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """Token login, get an access token for future requests."""

    if request.headers.get("content-type", "").startswith("application/json"):
        login_data = LoginRequest.model_validate(await request.json())
    else:
        form = await request.form()
        login_data = LoginRequest(
            email=form.get("email") or form.get("username", ""),
            password=form.get("password", ""),
        )
    if not login_data.email or not login_data.password:
        raise HTTPException(status_code=422, detail="Missing email or password")

    user = crud.authenticate_user(
        db, email=login_data.email, password=login_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not crud.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=settings.ENVIRONMENT == "production",
    )
    return {"message": "Login successful"}
