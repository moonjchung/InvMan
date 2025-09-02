from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import sentry_sdk

from app.core.config import settings
from app.core.limiter import limiter
from app.api.endpoints import (
    auth,
    items,
    categories,
    suppliers,
    users,
    purchase_orders,
    sales_orders,
    reports,
    dashboard,
)

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=1.0,
    )

origins = ["http://localhost:3000", "https://*.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])
app.include_router(
    purchase_orders.router, prefix="/purchase-orders", tags=["purchase-orders"]
)
app.include_router(sales_orders.router, prefix="/sales-orders", tags=["sales-orders"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])


@app.get("/healthz")
def read_root():
    return {"status": "ok"}