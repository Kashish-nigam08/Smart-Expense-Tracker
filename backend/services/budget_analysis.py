import pandas as pd

from models import Transaction, Budget


def get_budget_status(
    db,
    user_id: int
):

    budgets = db.query(Budget).filter(
        # Single-user application for the current version
        Budget.user_id == user_id
    ).all()

    transactions = db.query(Transaction).filter(
        # Single-user application for the current version
        Transaction.user_id == user_id,
        Transaction.transaction_type == "expense"
    ).all()

    if not budgets:
        return []

    transaction_data = [
        {
            "date": transaction.date,
            "category": transaction.category,
            "amount": transaction.amount
        }
        for transaction in transactions
    ]

    df = pd.DataFrame(transaction_data)

    results = []

    for budget in budgets:

        spent = 0

        if not df.empty:

            budget_transactions = df[
                (df["category"] == budget.category)
                & (pd.to_datetime(df["date"]).dt.month == budget.month)
                & (pd.to_datetime(df["date"]).dt.year == budget.year)
            ]

            spent = budget_transactions["amount"].sum()

        remaining = budget.budget_amount - spent

        usage_percentage = (
            (spent / budget.budget_amount) * 100
            if budget.budget_amount > 0
            else 0
        )

        if usage_percentage > 100:
            status = "Exceeded"
        elif usage_percentage >= 80:
            status = "Near Limit"
        else:
            status = "Within Budget"

        results.append({
            "category": budget.category,
            "month": budget.month,
            "year": budget.year,
            "budget": round(budget.budget_amount, 2),
            "spent": round(float(spent), 2),
            "remaining": round(float(remaining), 2),
            "usage_percentage": round(
                float(usage_percentage), 2
            ),
            "status": status
        })

    return results