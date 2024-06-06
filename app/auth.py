from .crypt import crypt_context


def verify_password(plain_password: str, hashed_password: str):
    return crypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return crypt_context.hash(password)
