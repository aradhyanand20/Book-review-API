from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from .models import Book
from src.config import config
from datetime import datetime
from uuid import UUID


DATABASE_URL=config.DATABASE_URL
class BookService:
    async def get_all_books(self,session:AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid:UUID,session:AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None
    
    async def create_book(self,book_data: BookCreateModel,  session:AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(
            **book_data_dict
        )
        # new_book.published_date = datetime.UUIDptime(book_data_dict['published_date'],"%Y-%m-%d")
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book
         
    async def update_book(self,book_uid:UUID,book_data: BookUpdateModel, session:AsyncSession):
        book_to_update =  await self.get_book(book_uid,session)
        if book_to_update is not None:
            update_date_dict = book_data.model_dump(exclude_unset=True)

            for k, v in update_date_dict.items():
                setattr(book_to_update,k,v)

            await session.commit()
            await session.refresh(book_to_update)
            return book_to_update
        else:
            return None



    async def delete_book(self,book_uid:UUID, session:AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        
        else:
            return None


 	
# Response body
# Download
# {
#   "message": "Login successful",
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjoiYXJhZGh5YW5hbmQyMEBnbWFpbC5jb20iLCJ1c2VyX3VpZCI6ImJkNjY0ZjFmLTZjZjEtNGE2Yi04ODdhLWJkNzA1ZmRkMThjOSJ9LCJleHAiOjE3NzI0NjY4MzcsImp0aSI6IjBmNjRhMTU1LTBkZjktNDk4Yy1iYTFhLTc3YWQ2MzAyOTc4NyIsInJlZnJlc2giOmZhbHNlfQ.CYGbPTamlrOsYbJDG-IzZ_NrzVFX2gZxSWxdXa-oWWo",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjoiYXJhZGh5YW5hbmQyMEBnbWFpbC5jb20iLCJ1c2VyX3VpZCI6ImJkNjY0ZjFmLTZjZjEtNGE2Yi04ODdhLWJkNzA1ZmRkMThjOSJ9LCJleHAiOjE3NzI2MzYwMzcsImp0aSI6IjE1YjQ3ZmZjLTk1OWMtNDAzOC1hOWJhLTQyZDczNWJhZmYxZCIsInJlZnJlc2giOnRydWV9.OAmOhaTx3rFriQHYL9AxzAHVD53FiMcHkX4CZa5En-I",
#   "user": {
#     "email": "aradhyanand20@gmail.com",
#     "uid": "bd664f1f-6cf1-4a6b-887a-bd705fdd18c9"
#   }
# }