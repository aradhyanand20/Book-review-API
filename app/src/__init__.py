from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
# from src.auth.models import User
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tag_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.db.models import User
from src.db.models import Book
from src.db.models import Review
from src.db.models import Tags
from .errors import (
    create_exception_handler,
    InvalidCredentials,
    TagAlreadyExists,
    TagNotFound,
    BookNotFound,
    UserAlreadyExists,
    InsufficientPermission,
    AccessTokenRequired,
    InvalidToken,
    RefreshTokenRequired,
    RevokedToken,
    UserNotFound
)

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server is starting. . . .")
    await init_db()
    yield
    print("Server has been stopped")


ver = "v1"
app = FastAPI(
    title="Bookly",
    description=" A REST API for the book review web service",
    version= ver,
    swagger_ui_parameters={"persistAuthorization": True}
)

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code= status.HTTP_403_FORBIDDEN,
        initial_detail={
            "message":"User with email already exists",
            "error_code":"user_exists"
        }
    )
)

app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        initial_detail={
            "message":"UserNot Found",
            "error_code":"user_not_found"
        }
    )
    
)
app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book not found",
                "error_code": "book_not_found",
            },
        ),
    )

app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )
app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )
app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )
app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )
app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Tag Not Found", "error_code": "tag_not_found"},
        ),
    )
app.add_exception_handler(
        TagAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Tag Already exists",
                "error_code": "tag_exists",
            },
        ),
    )
app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book Not Found",
                "error_code": "book_not_found",
            },
        ),
    )

@app.exception_handler(500)
async def internal_server_error(request,exc):
    return JSONResponse(
        content={"message":"Oops! Somrthing went wrong","error_code":"server_error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

app.include_router(book_router,prefix=f"/api/{ver}/books", tags=['books'])
app.include_router(auth_router,prefix=f"/api/{ver}/auth", tags=['auth'])
app.include_router(review_router,prefix=f"/api/{ver}/reviews", tags=['reviews'])
app.include_router(tag_router,prefix=f"/api/{ver}/tags", tags=['tags'])
