from sqlalchemy import create_engine, String,Integer, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


#base
class Base(DeclarativeBase):
    pass

#model
class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(Integer,primary_key=True)
    name:Mapped[str]= mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"<User id = {self.id} name = {self.name}, age = {self.age}>"
    

#engine    
engine = create_engine("sqlite:///mydb.db", echo = True)


#create tables
Base.metadata.create_all(engine)


# -- create--
with Session(engine) as session:
    session.add_all([
        User(name="Aradhya", age =27),
        User(name="charlie", age =17),
        User(name="sarooj", age =21),
        User(name="eve", age =22),
        User(name="Anamd", age =37),
    ])
    session.commit() #saves to the database



# --read--
with Session(engine) as session:
    stmt = select(User).where(User.age >=20, User.name !="eve")
    users = session.scalars(stmt).all()
    print("age 20+ ", users)
  
    
# --update--
with Session(engine) as session:
    stmt = select(User).order_by(User.age).limit(2)
    users = session.scalars(stmt).all()
    print("sorted age",users)

# --Delete--
with Session(engine) as session:
    stmt = select(User).where(User.name == "Aradhya")
    users = session.scalars(stmt).first()
    print("First match:", users)
    





    