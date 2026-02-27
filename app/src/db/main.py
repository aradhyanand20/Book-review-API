from sqlmodel import  SQLModel
from src.config import config
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
# from sqlmodel.ext.asyncio.session import 
from typing import AsyncGenerator



engine = create_async_engine(
            url = config.DATABASE_URL,
             echo =True)
Session = async_sessionmaker(
                bind= engine,
                class_ = AsyncSession,
                expire_on_commit= False
        )
async def init_db():
        async with engine.begin() as conn:
                from src.books.models import Book
                from src.auth.models import User
                
                await conn.run_sync(SQLModel.metadata.create_all)

async def get_session()->AsyncGenerator[AsyncSession, None]:
       async with Session() as session:
                yield session