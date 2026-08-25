from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services.expense_forecasting import forecast_next_month


router = APIRouter(
    prefix="/api/forecast",
    tags=["Expense Forecasting"]
)


@router.get("/")
def get_forecast(
    user_id: int,
    db: Session = Depends(get_db)
):

    return forecast_next_month(
        db,
        user_id
    )