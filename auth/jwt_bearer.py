from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_handler import decode_jwt


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        print("Credentials :", credentials)
        if credentials:
            if not credentials.scheme == "Bearer":
                print("Failed here.")
                raise HTTPException(status_code=403, detail="Invalid authentication token")

            if not self.verify_jwt(credentials.credentials):
                print("Failed here two")
                raise HTTPException(status_code=403, detail="Invalid token or expired token")

            return credentials.credentials
        else:
            print("Failed here three")
            raise HTTPException(status_code=403, detail="Invalid authorization token")

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwt_token)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
