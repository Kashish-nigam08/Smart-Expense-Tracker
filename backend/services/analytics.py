import pandas as pd
from sqlalchemy.orm import Session

from models import Transaction


def get_transaction_dataframe(
    db: Session,
    user_id: int
) -> pd.DataFrame:
    """Get transactions for a specific user."""

    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()

    if not transactions:
        return pd.DataFrame()

    data = [
        {
            "id": transaction.id,
            "date": transaction.date,
            "description": transaction.description,
            "amount": transaction.amount,
            "transaction_type": transaction.transaction_type,
            "category": transaction.category,
            "merchant": transaction.merchant
        }
        for transaction in transactions
    ]

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["date"])

    return df

def calculate_summary(db: Session,user_id: int):
    """Calculate overall financial summary."""

    df = get_transaction_dataframe(
    db,
    user_id
)

    if df.empty:
        return {
            "total_income": 0,
            "total_expenses": 0,
            "savings": 0,
            "savings_rate": 0,
            "total_transactions": 0,
            "average_transaction": 0
        }

    income = df[
        df["transaction_type"] == "income"
    ]["amount"].sum()

    expenses = df[
        df["transaction_type"] == "expense"
    ]["amount"].sum()

    savings = income - expenses

    savings_rate = (
        (savings / income) * 100
        if income > 0
        else 0
    )

    return {
        "total_income": round(float(income), 2),
        "total_expenses": round(float(expenses), 2),
        "savings": round(float(savings), 2),
        "savings_rate": round(float(savings_rate), 2),
        "total_transactions": len(df),
        "average_transaction": round(
            float(df["amount"].mean()), 2
        )
    }

def spending_by_category(
    db: Session,
    user_id: int
):
    """Calculate expenses grouped by category."""

    df = get_transaction_dataframe(
    db,
    user_id
)

    if df.empty:
        return []

    expenses = df[
        df["transaction_type"] == "expense"
    ]

    result = (
        expenses
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    return [
        {
            "category": category,
            "amount": round(float(amount), 2)
        }
        for category, amount in result.items()
    ]
def monthly_spending(
    db: Session,
    user_id: int
):
    """Calculate monthly expenses."""

    df = get_transaction_dataframe(
    db,
    user_id
)

    if df.empty:
        return []

    expenses = df[
        df["transaction_type"] == "expense"
    ].copy()

    expenses["month"] = expenses["date"].dt.strftime(
        "%Y-%m"
    )

    result = (
        expenses
        .groupby("month")["amount"]
        .sum()
        .sort_index()
    )

    return [
        {
            "month": month,
            "amount": round(float(amount), 2)
        }
        for month, amount in result.items()
    ]
def top_merchants(
    db: Session,
    user_id: int,
    limit: int = 5
):
    """Find merchants with the highest spending."""

    df = get_transaction_dataframe(
    db,
    user_id
)

    if df.empty:
        return []

    expenses = df[
        df["transaction_type"] == "expense"
    ]

    expenses = expenses[
        expenses["merchant"].notna()
        & (expenses["merchant"] != "")
    ]

    result = (
        expenses
        .groupby("merchant")["amount"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
    )

    return [
        {
            "merchant": merchant,
            "amount": round(float(amount), 2)
        }
        for merchant, amount in result.items()
    ]