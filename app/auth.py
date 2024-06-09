import jwt

from datetime import datetime, timezone, timedelta

from .crypt import crypt_context
from . import SECRET_KEY, ALGORITHM, ISSUER, AUDIENCE


def verify_password(plain_password: str, hashed_password: str):
    return crypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return crypt_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire_datetime = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire_datetime, "iss": ISSUER, "aud": AUDIENCE})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def decode_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[
                         ALGORITHM], audience=AUDIENCE, issuer=ISSUER)
    return payload
