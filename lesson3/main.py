from fastapi import FastAPI, HTTPException # type: ignore 
from typing import Optional, List, Dict # Імпортуємо Optional для необов'язкових параметрів
from pydantic import BaseModel # Імпортуємо BaseModel для валідації даних

app = FastAPI() # Створення екземпляру FastAPI

class User(BaseModel): # Створюємо модель для користувача
    id: int
    name: str
    email: str
    password: str

class Post(BaseModel): # Створюємо модель для валідації даних
    id: int
    title: str
    content: str
    author: User # Використовуємо модель User для автора посту

users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "password": "password123"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "password": "password456"},
    {"id": 3, "name": "Alice Johnson", "email": "alice@example.com", "password": "password789"},
]

posts = [
    {"id": 1, "title": "First Post", "content": "This is the content of the first post.", "author": users[0]},
    {"id": 2, "title": "Second Post", "content": "This is the content of the second post.", "author": users[1]},
    {"id": 3, "title": "Third Post", "content": "This is the content of the third post.", "author": users[2]},  
]

@app.get("/items")
async def items() -> List[Post]:
    # Використовуємо Pydantic для валідації даних
    return [Post(**post) for post in posts]

@app.get("/items/{id}") # Динамічний параметр у шляху
async def items(id: int) -> Post:
    for post in posts:
        if post["id"] == id:
            return Post(**post) # Використовуємо Pydantic для валідації даних
    raise HTTPException(status_code=404, detail="Item not found") # Викидає помилку, якщо пост не знайдено

@app.get("/search") # Шлях для пошуку постів
async def search(post_id: Optional[int] = None ) -> Dict[str, Optional[Post]]: # Опціональний параметр
    if post_id:
        for post in posts:
            if post["id"] == post_id:
                return {"post": Post(**post)}
        raise HTTPException(status_code=404, detail="Post not found") 
    else:
        return {"message": None}



# Що я вивчив: HTTP запити