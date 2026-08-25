from sqlalchemy.orm import Session

from models import User
from services.auth import hash_password, verify_password


def create_user(
    db: Session,
    name: str,
    email: str,
    password: str
):
    """Create a new user."""

    email = email.strip().lower()

    # Check if email already exists
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return None

    hashed_password = hash_password(password)

    user = User(
        name=name.strip(),
        email=email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    """Authenticate a user using email and password."""

    email = email.strip().lower()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.password
    ):
        return None

    return user