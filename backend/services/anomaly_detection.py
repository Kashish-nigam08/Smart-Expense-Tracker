import pandas as pd
from sklearn.ensemble import IsolationForest

from models import Transaction


def detect_anomalies(
    db,
    user_id: int
):
    """
    Detect unusual expense transactions
    for a specific user.
    """

    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == "expense"
    ).all()

    if len(transactions) < 5:
        return []

    data = [
        {
            "id": transaction.id,
            "date": transaction.date,
            "description": transaction.description,
            "amount": transaction.amount,
            "category": transaction.category,
            "merchant": transaction.merchant
        }
        for transaction in transactions
    ]

    df = pd.DataFrame(data)

    X = df[["amount"]]

    model = IsolationForest(
        contamination=0.10,
        random_state=42
    )

    df["prediction"] = model.fit_predict(X)

    df["anomaly_score"] = model.decision_function(X)

    df["is_anomaly"] = (
        df["prediction"] == -1
    )

    anomalies = df[
        df["is_anomaly"]
    ].copy()

    results = []

    for _, row in anomalies.iterrows():

        results.append({
            "transaction_id": int(row["id"]),
            "date": str(row["date"]),
            "description": row["description"],
            "amount": round(
                float(row["amount"]),
                2
            ),
            "category": row["category"],
            "merchant": row["merchant"],
            "anomaly_score": round(
                float(row["anomaly_score"]),
                4
            ),
            "reason": (
                "Transaction amount is unusually high "
                "compared with your normal spending."
            )
        })

    return results