
from fastapi import FastAPI,Header
from typing import Optional
from pydantic import BaseModel
app = FastAPI()


text_posts = {1:{ "title":"new post","content":"cool test post"}}

@app.get("/posts")
def get_all_posts():
    return text_posts

@app.get('/greet/{name}')
async def greet_name(name:str,age:int) -> dict:
    return {"message":f"hello {name}","age":age}

# @app.get('/greet')
# async def greet_name(name:str,age:int) -> dict:
#     return {"message":f"hello {name}","age":age}

# @app.get("/greet")
# async def greet_name(name:str)-> dict: 
#     return {"message":f"hello {name}"}

@app.get("/greet")
async def greet_name(name:Optional[str]= "Users", age: int = 0)-> dict: 
    return {"message":f"hello {name}", "age":age}

# from fastapi import Query
# @app.get("/greet")
# async def greet_name(
#     name: Optional[str] = Query("Users"),
#     age: int = Query(..., gt=0)
# ):
#     return {"message": f"hello {name}", "age": age}

# item = [
#     {'id': 1, "name": "Item One"},
#     {'id': 2, "name": "Item two"},
#     {'id': 3, "name": "Item three"},

# ]

# @app.get("/helloworld")
# def hello_world():
#     return {"hello world"}

# @app.get("/items")
# def get_item():
#     return item

# @app.get("/items/{id}")
# def get_post(id:int):
#     return next((x for items in item if item['id']==id), None)

class BookCreateModel(BaseModel):
    title : str
    author : str

@app.post('/create_book')
async def create_book(book_data: BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }

@app.get('/get_headers', status_code=500)
async def get_headers(
    accept:str = Header(None),
    content_type: str = Header(None),
    user_agent:str  = Header(None),
    host: str = Header(None)
):
    request_header = {}
    request_header["Accept"] = accept
    request_header["Content-Type"] = content_type
    request_header["user_agent"] = user_agent
    request_header["Host"] = host
    return request_header 