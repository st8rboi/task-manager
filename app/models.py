# Файл с описанием моделей базы данных для приложения

# Импортируем экземпляр SQLAlchemy для работы с базой данных
from extensions import db, login_manager
# Импортируем datetime для работы с датой и временем
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# Класс модели задачи, наследуется от базовой модели SQLAlchemy
class Task(db.Model):
    """Модель задачи в базе данных"""

    # Название таблицы в базе данных (необязательно, по умолчанию используется имя класса в нижнем регистре)
    __tablename__ = 'tasks'

    # Поле ID - уникальный идентификатор задачи, первичный ключ
    id = db.Column(db.Integer, primary_key=True)
    
    # Поле заголовка задачи: 
    # - String(50): строка макс. длиной 50 символов
    # - nullable=False: обязательное поле (не может быть пустым)
    title = db.Column(db.String(50), nullable=False)
    
    # Поле описания задачи:
    # - String(200): строка макс. длиной 200 символов
    # - nullable=False: обязательное поле
    description = db.Column(db.String(200), nullable=False)
    
    # Поле статуса выполнения:
    # - Boolean: логическое значение (True/False)
    # - default=False: значение по умолчанию - не выполнена
    completed = db.Column(db.Boolean, default=False)
    
    # Поле дедлайна задачи:
    # - DateTime: хранит дату и время
    # - nullable=True: может быть пустым (необязательное поле)
    deadline = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='tasks')

    def __repr__(self):
        """Строковое представление объекта (для отладки)"""
        # Возвращает понятное строковое описание объекта задачи.
        # Пример: '<Task ID: 1, Заголовок: Покупки, Статус: Не выполнена>'
        return f'<Task ID: {self.id}, Заголовок: {self.title}, Статус: {"Выполнена" if self.completed else "Не выполнена"}>'
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)