from fastapi import FastAPI, HTTPException # type: ignore 
from typing import Optional # Імпортуємо Optional для необов'язкових параметрів

app = FastAPI() # Створення екземпляру FastAPI

@app.get("/") # Декоратор для обробки GET запиту на кореневий шлях
async def home() -> dict[str, str]: # Функція для обробки запиту та які дані вона повертає
    return {"message": "Hello, World!"} # Повертає JSON відповідь з повідомленням

@app.get("/contacts")
async def get_contacts() -> int:
    return 34

posts = [
    {"id": 1, "title": "First Post", "content": "This is the content of the first post."},
    {"id": 2, "title": "Second Post", "content": "This is the content of the second post."},
    {"id": 3, "title": "Third Post", "content": "This is the content of the third post."},  
]

@app.get("/items")
async def items() -> list:
    """
    Повертає список всіх постів.
    """
    return posts

@app.get("/items/{item_id}") # Динамічний параметр у шляху
async def items(id: int) -> dict:
    for post in posts:
        if post["id"] == id:
            return post
    raise HTTPException(status_code=404, detail="Item not found") # Викидає помилку, якщо пост не знайдено

@app.get("/search") # Шлях для пошуку постів
async def search(post_id: Optional[int] = None ) -> dict: # Опціональний параметр
    if post_id:
        for post in posts:
            if post["id"] == post_id:
                return post
        raise HTTPException(status_code=404, detail="Post not found") 
    else:
        return {"message": "No post ID provided"}



# Асинхроність дозволяє обробляти запити без блокування, що підвищує продуктивність.
# Що я вивчив: принцип роботи, документація, типи даних, асинхроність, вивід усіх постів
# Динамічні параметри, необов'язкові параметри.