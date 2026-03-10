from fastapi import FastAPI
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
app.include_router(book_router,prefix=f"/api/{ver}/books", tags=['books'])
app.include_router(auth_router,prefix=f"/api/{ver}/auth", tags=['auth'])
app.include_router(review_router,prefix=f"/api/{ver}/reviews", tags=['reviews'])
app.include_router(tag_router,prefix=f"/api/{ver}/tags", tags=['tags'])
