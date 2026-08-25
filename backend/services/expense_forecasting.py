import pandas as pd
from sklearn.linear_model import LinearRegression

from models import Transaction


def forecast_next_month(
    db,
    user_id: int
):
    """
    Forecast next month's expenses using
    historical monthly spending.
    """

    transactions = db.query(Transaction).filter(
    Transaction.user_id == user_id,
    Transaction.transaction_type == "expense"
).all()

    if len(transactions) < 5:
        return {
            "message": "Not enough transaction data for forecasting."
        }

    data = [
        {
            "date": transaction.date,
            "amount": transaction.amount
        }
        for transaction in transactions
    ]

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["date"])

    # Create monthly totals
    monthly = (
        df
        .set_index("date")
        .resample("ME")["amount"]
        .sum()
        .reset_index()
    )

    if len(monthly) < 3:
        return {
            "message": (
                "At least 3 months of expense data "
                "is recommended for forecasting."
            )
        }

    # Convert months into numerical values
    monthly["month_number"] = range(
        1,
        len(monthly) + 1
    )

    X = monthly[["month_number"]]

    y = monthly["amount"]

    # Create model
    model = LinearRegression()

    model.fit(X, y)

    # Predict next month
    next_month_number = len(monthly) + 1

    prediction = model.predict(
        [[next_month_number]]
    )[0]

    # Avoid negative prediction
    prediction = max(
        0,
        float(prediction)
    )

    # Determine next month
    last_month = monthly["date"].iloc[-1]

    next_month = (
        last_month + pd.DateOffset(months=1)
    )

    return {
        "next_month": next_month.strftime("%Y-%m"),
        "predicted_expenses": round(
            prediction,
            2
        ),
        "historical_months": len(monthly)
    }