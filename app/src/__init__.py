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
from .errors import register_all_errors
from .middleware import register_middleware

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
    lifespan=life_span,
    swagger_ui_parameters={"persistAuthorization": True}
)

@app.exception_handler(500)
async def internal_server_error(request,exc):
    return JSONResponse(
        content={"message":"Oops! Somrthing went wrong","error_code":"server_error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
        
register_all_errors(app)
register_middleware(app)

app.include_router(book_router,prefix=f"/api/{ver}/books", tags=['books'])
app.include_router(auth_router,prefix=f"/api/{ver}/auth", tags=['auth'])
app.include_router(review_router,prefix=f"/api/{ver}/reviews", tags=['reviews'])
app.include_router(tag_router,prefix=f"/api/{ver}/tags", tags=['tags'])
