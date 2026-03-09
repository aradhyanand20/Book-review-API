from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.db.models import Tags
from .schemas import TagAddModel, TagCreateModel
from uuid import UUID

book_service = BookService()

server_error = HTTPException(
    status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="SOMETHING WENT OFF"
)
class TagService:
    async def get_tags(self,session:AsyncSession):
        statement = select(Tags).order_by(desc(Tags.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def add_tag_to_books(self,book_uid:str,tag_data:TagAddModel,session:AsyncSession):
        book = await book_service.get_book(book_uid=book_uid, session=session)
        if not book:
            raise HTTPException(status_code=404, detail="book not found")
        
        for tag_item in tag_data.tags:
            result = await session.exc(
                select(Tags).
            )
            result = await session
        

 
    
