from sqlmodel import SQLModel, Field, Column, Relationship
# from src.auth import models
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime,date, timezone
import uuid
from typing import Optional
datetime.now()

class Book(SQLModel, table= True):
    __tablename__ ="books"
    uid: uuid.UUID= Field(
        default_factory= uuid.uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable = False,
            primary_key =True,
            
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None,foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True)), default_factory=lambda: datetime.now(timezone.utc))
    update_at: datetime= Field(sa_column=Column(pg.TIMESTAMP(timezone=True)), default_factory=lambda: datetime.now(timezone.utc))
    user: Optional["User"] = Relationship(back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"
