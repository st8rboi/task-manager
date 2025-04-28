# Импорт необходимых модулей
from flask import Flask, render_template, Blueprint, request, redirect, url_for, abort
from models import Task  # Импорт модели задачи
from extensions import db
from datetime import datetime  # Для работы с датой/временем
from routes.tasks import tasks_bp 
import os

# Инициализация Flask-приложения
templates_dir = os.path.abspath('../templates')
app = Flask(__name__, template_folder=templates_dir)
app.register_blueprint(tasks_bp)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Путь к SQLite-базе
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение трекинга модификаций
db.init_app(app)  # Инициализация БД в приложении

# Маршрут для главной страницы
@app.route('/')
@app.route('/<filter>')  # Поддержка фильтрации задач
def index(filter='all'):
    """
    Отображает список задач с возможностью фильтрации
    
    Параметры:
    filter (str): Тип фильтра ('completed', 'pending', 'all')
    
    Возвращает:
    HTML-страницу с отфильтрованными задачами
    """
    # Определение задач по фильтру
    match filter:
        case 'completed':
            tasks = Task.query.filter_by(completed=True).all()
        case 'pending':
            tasks = Task.query.filter_by(completed=False).all()
        case _:
            tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    with app.app_context():
        if not os.path.exists('tasks.db'):
            db.create_all()
    app.run(debug=True)