from datetime import date

import pandas as pd

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File
)

from sqlalchemy.orm import Session

from database import get_db
from models import Transaction

from services.data_processing import (
    clean_transactions,
    categorize_transaction
)


router = APIRouter(
    prefix="/api/transactions",
    tags=["Transactions"]
)

@router.post("/")
def add_transaction(
    transaction_date: date,
    description: str,
    amount: float,
    transaction_type: str,
    category: str | None = None,
    merchant: str | None = None,
    db: Session = Depends(get_db)
):
    transaction = Transaction(
        user_id=1,
        date=transaction_date,
        description=description,
        amount=amount,
        transaction_type=transaction_type,
        category=category,
        merchant=merchant
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


@router.get("/")
def get_transactions(
    user_id: int,
    db: Session = Depends(get_db)
):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()

    return transactions


@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


@router.put("/{transaction_id}")
def update_transaction(
    transaction_id: int,
    transaction_date: date,
    description: str,
    amount: float,
    transaction_type: str,
    category: str | None = None,
    merchant: str | None = None,
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    transaction.date = transaction_date
    transaction.description = description
    transaction.amount = amount
    transaction.transaction_type = transaction_type
    transaction.category = category
    transaction.merchant = merchant

    db.commit()
    db.refresh(transaction)

    return transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return {
        "message": "Transaction deleted successfully"
    }
@router.post("/upload")
async def upload_transactions(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload CSV or Excel transaction data,
    clean it, categorize it and prevent duplicates.
    """

    filename = file.filename.lower()

    if not (
        filename.endswith(".csv")
        or filename.endswith(".xlsx")
        or filename.endswith(".xls")
    ):
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are supported"
        )

    try:
        # Read uploaded file
        contents = await file.read()

        from io import BytesIO

        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
        else:
            df = pd.read_excel(BytesIO(contents))

        # Clean the data
        df = clean_transactions(df)

        imported_count = 0
        duplicate_count = 0

        # Keep track of transactions in this upload
        uploaded_transactions = set()

        for _, row in df.iterrows():

            # -------------------------------
            # Normalize transaction values
            # -------------------------------

            transaction_date = row["date"].date()

            description = str(
                row["description"]
            ).strip().lower()

            amount = round(
                float(row["amount"]),
                2
            )

            transaction_type = str(
                row["transaction_type"]
            ).strip().lower()

            # -------------------------------
            # Create unique transaction key
            # -------------------------------

            transaction_key = (
                transaction_date,
                description,
                amount,
                transaction_type
            )

            # Duplicate inside uploaded file
            if transaction_key in uploaded_transactions:
                duplicate_count += 1
                continue

            uploaded_transactions.add(
                transaction_key
            )

            # -------------------------------
            # Check database for duplicate
            # -------------------------------

            existing_transactions = db.query(
                Transaction
            ).filter(
                # Single-user application for the current version
                Transaction.user_id == user_id,
                Transaction.date == transaction_date,
                Transaction.amount == amount,
                Transaction.transaction_type == transaction_type
            ).all()

            duplicate_found = False

            for existing in existing_transactions:

                existing_description = str(
                    existing.description
                ).strip().lower()

                if existing_description == description:
                    duplicate_found = True
                    break

            if duplicate_found:
                duplicate_count += 1
                continue

            # -------------------------------
            # Category
            # -------------------------------

            category = str(
                row["category"]
            ).strip()

            if not category:
                category = categorize_transaction(
                    description
                )

            # -------------------------------
            # Merchant
            # -------------------------------

            merchant = row["merchant"]

            if pd.isna(merchant):
                merchant = None
            else:
                merchant = str(
                    merchant
                ).strip()

            # -------------------------------
            # Create transaction
            # -------------------------------

            transaction = Transaction(
                # Single-user application for the current version
                user_id=user_id,
                date=transaction_date,
                description=description,
                amount=amount,
                transaction_type=transaction_type,
                category=category,
                merchant=merchant
            )

            db.add(transaction)

            imported_count += 1

        # Save new transactions
        db.commit()

        return {
            "message": "File processed successfully",
            "transactions_imported": imported_count,
            "duplicates_skipped": duplicate_count
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=f"Error processing file: {str(e)}"
        )