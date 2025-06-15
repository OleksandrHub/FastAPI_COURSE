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

class PostCreate(BaseModel): # Модель для створення посту
    title: str
    content: str
    author_id: int # Замість повного об'єкту User, використовуємо лише ID автора

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

@app.post("/items/add", response_model=Post) # Додаємо новий пост response_model для валідації відповіді
async def add_item(post: PostCreate) -> Post:
    author = next((user for user in users if user["id"] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_post = {
        "id": len(posts) + 1, # Генеруємо новий ID
        "title": post.title,
        "content": post.content,
        "author": author
    }
    posts.append(new_post) # Додаємо новий пост до списку
    return Post(**new_post)

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

# get запит коли ми заходимо на сторінку
# post запит коли ми відправляємо дані на сервер
# put запит коли ми змінюємо дані на сервері
# delete запит коли ми видаляємо дані з сервера

# Що я вивчив: Pydantic для валідації даних,