from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.budget_analysis import get_budget_status
from database import get_db
from models import Budget
from schemas import BudgetCreate, BudgetResponse


router = APIRouter(
    prefix="/api/budgets",
    tags=["Budgets"]
)


@router.post(
    "/",
    response_model=BudgetResponse
)
def create_budget(
    user_id: int,
    budget_data: BudgetCreate,
    db: Session = Depends(get_db)
):

    # Check whether a budget already exists
    existing_budget = db.query(Budget).filter(
        # Single-user application for the current version
        Budget.user_id == user_id,
        Budget.category == budget_data.category,
        Budget.month == budget_data.month,
        Budget.year == budget_data.year
    ).first()

    if existing_budget:
        raise HTTPException(
            status_code=400,
            detail="Budget already exists for this category and month"
        )

    budget = Budget(
        # Single-user application for the current version
        user_id=user_id,
        category=budget_data.category,
        budget_amount=budget_data.budget_amount,
        month=budget_data.month,
        year=budget_data.year
    )

    db.add(budget)
    db.commit()
    db.refresh(budget)

    return budget


@router.get("/")
def get_budgets(
    user_id: int,
    db: Session = Depends(get_db)
):

    budgets = db.query(Budget).filter(
        Budget.user_id == user_id
    ).all()

    return budgets

@router.get("/status")
def budget_status(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_budget_status(
        db,
        user_id
    )

@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    budget = db.query(Budget).filter(
        Budget.id == budget_id,
# Single-user application for the current version
        Budget.user_id == user_id
    ).first()

    if not budget:
        raise HTTPException(
            status_code=404,
            detail="Budget not found"
        )

    db.delete(budget)
    db.commit()

    return {
        "message": "Budget deleted successfully"
    }