from pydantic import BaseModel, Field
from typing import Annotated

class UserBD(BaseModel): # Створюємо модель для користувача
    name: str
    email: str
    password: str

class User(UserBD): # Створюємо модель для користувача
    id: int

    class Config: # Налаштовуємо конфігурацію Pydantic
        orm_mode = True # Дозволяємо Pydantic використовувати ORM-моделі для валідації даних

class UserCreate(UserBD):
    pass

class PostBD(BaseModel): # Створюємо модель для валідації даних
    title: str
    content: str
    author_id: int

class PostCreate(PostBD): # Модель для створення посту
    pass

class Post(PostBD): # Створюємо модель для посту
    id: int
    author: User # Додаємо автора посту

    class Config: # Налаштовуємо конфігурацію Pydantic
        orm_mode = True