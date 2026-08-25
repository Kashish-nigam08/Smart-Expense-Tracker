from fastapi import FastAPI
from sqlalchemy import text
from database import engine, Base
from routers.transactions import router as transaction_router
from routers.analytics import router as analytics_router
from routers.budgets import router as budget_router
from routers.anomalies import router as anomaly_router
from routers.forecast import router as forecast_router
from routers.auth import router as auth_router
app = FastAPI(
    title="Smart Expense & Financial Analytics Platform",
    description="An intelligent platform for expense tracking, analytics, anomaly detection and financial insights.",
    version="1.0.0"
)


app.include_router(transaction_router)
app.include_router(analytics_router)
app.include_router(budget_router)
app.include_router(anomaly_router)
app.include_router(forecast_router)
app.include_router(auth_router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Smart Expense & Financial Analytics Platform API is running"
    }


@app.get("/health")
def health_check():

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

