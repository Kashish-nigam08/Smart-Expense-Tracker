from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from services.anomaly_detection import (
    detect_anomalies
)


router = APIRouter(
    prefix="/api/anomalies",
    tags=["Anomaly Detection"]
)


@router.get("/")
def get_anomalies(
    user_id: int,
    db: Session = Depends(get_db)
):

    return detect_anomalies(
        db,
        user_id
    )