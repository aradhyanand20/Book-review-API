from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserModel, UserLoginModel,UserBookModel, EmailModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token, decode_token, verify_password, create_url_safe_token,decode_url_safe_token
from datetime import timedelta, datetime, timezone
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist
from src.mail import create_message, mail
from src.config import config
from src.errors import UserAlreadyExists,UserNotFound, InvalidCredentials,InvalidToken



auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])


REFRESH_TOKEN_EXPIRY = 2


@auth_router.post("/send-email")
async def send_email(emails:EmailModel):
    emails = emails.addresses
    html = "<h1>Welcome to bookly</h1>"
    message = create_message(
        recipients=emails,
        subject="Welcome",
        body=html
    )
    await mail.send_message(message)
@auth_router.post('/signup',
                  status_code= status.HTTP_201_CREATED)
async def create_user_account(user_data:UserCreateModel,
 session:AsyncSession= Depends(get_session) ):
    email = user_data.email
    user_exists = await user_service.user_exists(email,session)

    if user_exists:
        raise UserAlreadyExists
    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email":email})
    
    link = f"http://127.0.0.1:8000/api/v1/auth/verify/{token}"
    html_message = f"""
<html>
<body>
<h1>Verify your email</h1>
<p>
Click below to verify your email:<br>
<a href="{link}">Verify Email</a>
</p>
</body>
</html>
"""

    message = create_message(
        recipients=[email],
        subject="verify your email",
        body=html_message
    )
    await mail.send_message(message)
    return {
        "message":"Account Created! Check email to verify your account",
        "user": new_user
    }

@auth_router.get('/verify/{token}')
async def verify_user_account(token:str, session:AsyncSession= Depends(get_session)):
    token_data = decode_url_safe_token(token)
    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(user_email,session)
        if not user:
            raise UserNotFound()
        await user_service.update_user(user, {'is_verified': True}, session)
        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={"message": "Error occurred during the varification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post('/login')
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    
    user = await user_service.get_user_by_email(email,session)

    if user is not None:
        password_valid = verify_password(password,user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    
                    'email': user.email,
                    'user_uid': str(user.uid) ,
                    'role': user.role
                    }  
                
                )
            
            refresh_token = create_access_token(
                 user_data={
                               
                      'email': user.email,
                      'user_uid': str(user.uid)
                  
                 },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message":"Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":{
                        "email": user.email,
                        "uid": str(user.uid)
                    }

                }
            )
    raise InvalidCredentials  
            
   
   
@auth_router.get('/refresh_token')
async def get_new_access_token(token_details:dict= Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    # if datetime.fromtimestamp(expiry_timestamp)> datetime.now():
    # After
    if datetime.fromtimestamp(expiry_timestamp, tz=timezone.utc) > datetime.now(tz=timezone.utc):
        new_access_token = create_access_token(
            user_data= token_details['user']
        )
        return JSONResponse(content={
            "access_token": new_access_token
        })
    raise InvalidToken

@auth_router.get('/me', response_model=UserBookModel)
async def get_me(user= Depends(get_current_user),_: bool = Depends(role_checker)):
    return user

@auth_router.get('/logout')
async def revoke_token(token_details:dict= Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message":"Logged out successfully",
        },
        status_code= status.HTTP_200_OK
    )