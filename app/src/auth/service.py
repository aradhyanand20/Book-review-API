from .models import User
from.schemas import UserCreateModel
from .utils import generate_passwd_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import  select

class UserService:
    async def get_user_by_email(self,email:str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user
    async def user_exists(self,email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user is not None else False
    
    async def create_user(self, user_data: UserCreateModel, session:AsyncSession):
        user_data_dict = user_data.model_dump()
        user_data_dict.pop('password') 
        user_data_dict['password_hash'] = generate_passwd_hash(user_data.password) 

        new_user = User(
            **user_data_dict
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user
    

#     {
#   "message": "Login successful",
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjoiYXJhZGh5YW5hbmQyMEBnbWFpbC5jb20iLCJ1c2VyX3VpZCI6ImJkNjY0ZjFmLTZjZjEtNGE2Yi04ODdhLWJkNzA1ZmRkMThjOSJ9LCJleHAiOjE3NzIzODMwNzUsImp0aSI6ImNmZjE0OTgyLWY4MTEtNGFmYS05NzRlLWQwYjEyOWI3NDBhZCIsInJlZnJlc2giOmZhbHNlfQ.Vhg6rF2YI0EroOpviEgxWfJ4aYXgLO-lu0hxikW3O7Y",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjoiYXJhZGh5YW5hbmQyMEBnbWFpbC5jb20iLCJ1c2VyX3VpZCI6ImJkNjY0ZjFmLTZjZjEtNGE2Yi04ODdhLWJkNzA1ZmRkMThjOSJ9LCJleHAiOjE3NzI1NTIyNzUsImp0aSI6ImViMDA4YmNiLWFmY2QtNDYxNy1iNDhiLTljOWQ5ZDlkNmViYSIsInJlZnJlc2giOnRydWV9.YL02niHQkhb-iW2sEn7m_LJkGWnyLsY3u4M3INdrTw4",
#   "user": {
#     "email": "aradhyanand20@gmail.com",
#     "uid": "bd664f1f-6cf1-4a6b-887a-bd705fdd18c9"
 