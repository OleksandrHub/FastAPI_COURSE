from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship # Для встановлення зв'язків між моделями
from database import Base  # Імпортуємо базовий клас для моделей бази даних

class User(Base):  # Створюємо модель для користувача
    __tablename__ = "users"  # Вказуємо назву таблиці в базі даних

    id = Column(Integer, primary_key=True, index=True)  # Ідентифікатор користувача
    name = Column(String, index=True)  # Ім'я користувача
    email = Column(String, unique=True, index=True)  # Електронна пошта користувача
    password = Column(String)  # Пароль користувача

    posts = relationship("Post", back_populates="author")  # Встановлюємо зв'язок з моделлю Post

class Post(Base):  # Створюємо модель для посту
    __tablename__ = "posts" # Вказуємо назву таблиці в базі даних

    id = Column(Integer, primary_key=True, index=True)  # Ідентифікатор посту
    title = Column(String, index=True)  # Заголовок посту
    content = Column(String)  # Зміст посту
    author_id = Column(Integer, ForeignKey("users.id"))  # Ідентифікатор автора посту

    author = relationship("User")  # Встановлюємо зв'язок з моделлю User