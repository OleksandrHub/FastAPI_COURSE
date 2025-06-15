from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends # type: ignore 
from typing import Optional, List, Dict, Annotated # Імпортуємо Optional для необов'язкових параметрів
from sqlalchemy.orm import Session # Імпортуємо Session для роботи з базою даних

from models import User, Post, Base # Імпортуємо моделі з файлу models.py
from database import engine, session_local # Імпортуємо базу даних та сесію з файлу database.py
from schemas import UserCreate, PostCreate, Post as PostSchema, User as UserSchema # Імпортуємо схеми з файлу schemas.py

app = FastAPI() # Створення екземпляру FastAPI

Base.metadata.create_all(bind=engine) # Створюємо таблиці в базі даних, якщо їх ще немає

def get_db():
    db = session_local() # Створюємо сесію для роботи з базою даних
    try:
        yield db # Повертаємо сесію для використання в запитах
    finally:
        db.close() # Закриваємо сесію після використання

@app.post("/users/add", response_model=UserSchema) # Додаємо нового користувача, response_model для валідації відповіді
async def add_user(user: UserCreate, db: Session = Depends(get_db)) -> UserSchema: # Додаємо нового користувача Depends для отримання сесії бази даних
    db_user = User(name=user.name, email=user.email, password=user.password) # Створюємо нового користувача
    db.add(db_user) # Додаємо користувача до сесії
    db.commit() # Зберігаємо зміни в базі даних
    db.refresh(db_user) # Оновлюємо користувача після коміту
    return db_user # Повертаємо користувача у форматі Pydantic

@app.post("/posts/add", response_model=PostSchema) # Додаємо нового користувача, response_model для валідації відповіді
async def post_create(post: PostCreate, db: Session = Depends(get_db)) -> PostSchema: # Додаємо нового користувача Depends для отримання сесії бази даних
    db_user = db.query(User).filter(User.id == post.author_id).first() # Перевіряємо, чи існує автор посту
    if not db_user: # Якщо автор не знайдений, повертаємо помилку 404
        raise HTTPException(status_code=404, detail="Author not found")
    db_post = Post(title=post.title, content=post.content, author_id=post.author_id) # Створюємо нового користувача
    db.add(db_post) # Додаємо користувача до сесії
    db.commit() # Зберігаємо зміни в базі даних
    db.refresh(db_post) # Оновлюємо користувача після коміту
    return db_post # Повертаємо користувача у форматі Pydantic

@app.get("/posts", response_model=List[PostSchema]) # Отримуємо список постів
async def get_posts(db: Session = Depends(get_db)) -> List[PostSchema]:
    posts = db.query(Post).all()
    return posts

# Що я вивчив:  Робота з Базами Даних, ORM, SQLAlchemy, Alembic
# schemas.py - це файл, який містить схеми для валідації даних за допомогою Pydantic.
# models.py - це файл, який містить моделі для роботи з базою даних за допомогою SQLAlchemy.
# main.py - це файл, який містить основний код для запуску FastAPI додатку.
# database.py - це файл, який містить код для підключення до бази даних та створення таблиць.
# pip install sqlalchemy, sqlite 