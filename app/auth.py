from datetime import datetime, timedelta
from jose import jwt, JWTError

from .crypt import crypt_context
from . import SECRET_KEY, ALGORITHM, ISSUER, AUDIENCE


def verify_password(plain_password: str, hashed_password: str):
    return crypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return crypt_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire_datetime = datetime.now(datetime.UTC) + expires_delta
    to_encode.update({"exp": expire_datetime, "iss": ISSUER, "aud": AUDIENCE})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
