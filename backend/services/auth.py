import bcrypt


def hash_password(password: str) -> str:
    """Hash a password before storing it in the database."""

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(
    password: str,
    hashed_password: str
) -> bool:
    """Check whether the entered password matches the stored hash."""

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )