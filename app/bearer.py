from fastapi import Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError, ExpiredSignatureError

from .auth import decode_access_token


class JwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme")
            try:
                decode_access_token(credentials.credentials)
                return credentials.credentials
            except ExpiredSignatureError:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Token has expired")
            except InvalidTokenError:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code")
