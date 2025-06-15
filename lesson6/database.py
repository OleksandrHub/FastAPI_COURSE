from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_BD_URL = "sqlite:///./test.db"  # URL для підключення до бази даних SQLite

engine = create_engine(SQL_BD_URL, connect_args={"check_same_thread": False})  # Створюємо движок бази даних
# що це означає: connect_args={"check_same_thread": False} - це параметр, який дозволяє використовувати базу даних з кількох потоків.

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Створюємо сесію для роботи з базою даних
# що це означає: autocommit=False - це параметр, який дозволяє не виконувати коміт автоматично після кожної операції з базою даних.
# autoflush=False - це параметр, який дозволяє не виконувати флаш автоматично після кожної операції з базою даних.
# bind=engine - це параметр, який дозволяє прив'язати сесію до движка бази даних.

Base = declarative_base()  # Створюємо базовий клас для моделей бази даних