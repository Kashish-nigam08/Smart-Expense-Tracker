from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from services.analytics import (
    calculate_summary,
    spending_by_category,
    monthly_spending,
    top_merchants
)


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


@router.get("/summary")
def summary(
    user_id: int,
    db: Session = Depends(get_db)
):
    return calculate_summary(
        db,
        user_id
    )

@router.get("/categories")
def categories(
    user_id: int,
    db: Session = Depends(get_db)
):
    return spending_by_category(
        db,
        user_id
    )

@router.get("/monthly")
def monthly(
    user_id: int,
    db: Session = Depends(get_db)
):
    return monthly_spending(
        db,
        user_id
    )

@router.get("/top-merchants")
def merchants(
    user_id: int,
    db: Session = Depends(get_db)
):
    return top_merchants(
        db,
        user_id
    )