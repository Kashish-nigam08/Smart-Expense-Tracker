import pandas as pd


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare transaction data.
    """

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Required columns
    required_columns = [
        "date",
        "description",
        "amount",
        "transaction_type"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Convert date
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Convert amount to numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Remove rows with invalid date or amount
    df = df.dropna(
        subset=["date", "amount"]
    )

    # Clean description
    df["description"] = (
        df["description"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    # Clean transaction type
    df["transaction_type"] = (
        df["transaction_type"]
        .fillna("expense")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Standardize transaction type
    df["transaction_type"] = df[
        "transaction_type"
    ].replace({
        "debit": "expense",
        "credit": "income",
        "withdrawal": "expense",
        "deposit": "income"
    })

    # Add category column if missing
    if "category" not in df.columns:
        df["category"] = None

    # Add merchant column if missing
    if "merchant" not in df.columns:
        df["merchant"] = None

    # Clean category and merchant
    df["category"] = df["category"].fillna("").astype(str).str.strip()

    df["merchant"] = df["merchant"].fillna("").astype(str).str.strip()

    # Remove duplicate transactions
    df = df.drop_duplicates(
        subset=[
            "date",
            "description",
            "amount",
            "transaction_type"
        ]
    )

    return df
def categorize_transaction(description: str) -> str:
    """
    Automatically categorize a transaction
    based on its description.
    """

    description = description.lower()

    categories = {
        "Food": [
            "zomato",
            "swiggy",
            "restaurant",
            "food",
            "dominos",
            "pizza",
            "cafe"
        ],

        "Shopping": [
            "amazon",
            "myntra",
            "flipkart",
            "shopping",
            "mall"
        ],

        "Transport": [
            "uber",
            "ola",
            "metro",
            "fuel",
            "petrol",
            "transport"
        ],

        "Entertainment": [
            "netflix",
            "spotify",
            "movie",
            "cinema",
            "prime video"
        ],

        "Healthcare": [
            "hospital",
            "pharmacy",
            "medical",
            "doctor",
            "apollo"
        ],

        "Bills": [
            "electricity",
            "water bill",
            "internet",
            "jio",
            "airtel",
            "bill"
        ],

        "Salary": [
            "salary",
            "payroll"
        ]
    }

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in description:
                return category

    return "Other"