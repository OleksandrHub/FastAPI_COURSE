from fastapi import FastAPI, HTTPException, Path, Query, Body # type: ignore 
from typing import Optional, List, Dict, Annotated # Імпортуємо Optional для необов'язкових параметрів
from pydantic import BaseModel, Field # Імпортуємо BaseModel для валідації даних

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

class UserCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=1, max_length=100)] # Використовуємо Field для валідації параметрів запиту
    email: Annotated[str, Field(...)] # Регулярний вираз для валідації email
    password: Annotated[str, Field(..., min_length=6, max_length=100)] # Мінімальна довжина пароля


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

@app.post("/user/add", response_model=User) 
async def add_user(post: Annotated[UserCreate, Body(..., example={'name': 'John Doe', 'email': 'john@example.com', 'password': 'password123'})]) -> User:
    new_user = {
        "id": len(users) + 1, # Генеруємо новий ID
        "name": post.name,
        "email": post.email,
        "password": post.password
    }
    posts.append(new_user) # Додаємо нового користувача до списку
    return User(**new_user)

@app.get("/items/{id}") # Динамічний параметр у шляху
async def items(id: Annotated[int, Path(title="The ID of the item to get", ge=1, lt=100)]) -> Post:
    for post in posts:
        if post["id"] == id:
            return Post(**post) # Використовуємо Pydantic для валідації даних
    raise HTTPException(status_code=404, detail="Item not found") # Викидає помилку, якщо пост не знайдено

@app.get("/search") # Шлях для пошуку постів
async def search(post_id: Annotated[Optional[int], Query(title="Post ID", ge=1, le=100)]) -> Dict[str, Optional[Post]]: # Опціональний параметр
    if post_id:
        for post in posts:
            if post["id"] == post_id:
                return {"post": Post(**post)}
        raise HTTPException(status_code=404, detail="Post not found") 
    else:
        return {"message": None}

# Field - це функція, яка дозволяє додавати метадані до полів моделі Pydantic.
# Body - це функція, яка дозволяє вказати, що дані повинні бути передані в тілі запиту.
# Query (параметри запиту) є такими параметрами, які передаються в URL після знаку питання (?) і використовуються для фільтрації або пошуку даних.
# Path є такі параметри: ( для динамічних параметрів у шляху )
# - ... : Обов'язковий параметр, який повинен бути присутній у запиті
# - title: Назва параметра, яка буде відображатися в документації
# - ge: Мінімальне значення (greater than or equal)
# - le: Максимальне значення (less than or equal)
# - gt: Значення повинно бути більше (greater than)
# - lt: Значення повинно бути менше (less than)
# - description: Опис параметра, який буде відображатися в документації
# - deprecated: Позначає, що параметр застарілий і не рекомендується до використання
# - example: Приклад значення параметра, який буде відображатися в документації
# - alias: Альтернативна назва параметра, яка буде використовуватися в запитах
# - default: Значення за замовчуванням для параметра, якщо воно не вказано в запиті
# - regex: Регулярний вираз, який повинен відповідати значенню параметра
# - min_length: Мінімальна довжина рядка
# - max_length: Максимальна довжина рядка
# - pattern: Регулярний вираз, який повинен відповідати значенню параметра
# Що я вивчив:  Анотації та Валідація