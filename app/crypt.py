from passlib.context import CryptContext


def hash_password(password: str):
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(password)
