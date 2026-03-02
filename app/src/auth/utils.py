from passlib.context import CryptContext
from datetime import datetime,timedelta
import jwt
from src.config import config
import uuid
import logging
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRY = 3600

def generate_passwd_hash(password: str) -> str:
    return passwd_context.hash(password)  
def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data:dict, expiry:timedelta= None, refresh: bool= False):
    payload ={}
    payload['user'] = user_data
    payload['exp'] = datetime.now() +(expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    token_data = jwt.encode(
        payload=payload,
        key = config.JWT_SECRET,
        algorithm= config.JWT_ALGORITHM
    )
    return token_data

def decode_token(token:str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key= config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM]
        )
        return token_data
    
    except jwt.PyJWKError as e:
        logging.exception(e)
        return None
    except ExpiredSignatureError:
        return None