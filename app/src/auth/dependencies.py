from fastapi.security import HTTPBearer
from fastapi import Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException

class TokenBearer(HTTPBearer):
    
    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)

    async def __call__(self, request: Request)-> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token_data):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail= "Invalid or expired token"     
            )
        self.verify_token_data(token_data)
        return token_data
    def verify_token_data(self,token_data):
        raise NotImplementedError("Please override this method")    
    def token_valid(self, token_data) -> bool:
     return token_data is not None
    
class AccessTokenBearer(TokenBearer):
   def verify_token_data(self,token_data:dict) -> None:
         if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail= "Please provide access token"     
            )

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict) -> None:
         if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail= "Please provide a refresh token"     
            )
