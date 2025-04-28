# Импорт необходимых модулей
from flask import Flask, render_template, request, Blueprint, redirect, url_for, abort
from extensions import db  # Импорт объекта SQLAlchemy
from models import Task  # Импорт модели задачи
from datetime import datetime  # Для работы с датой/временем

tasks_bp = Blueprint('tasks', __name__)

# Маршрут для добавления задач
@tasks_bp.route('/add', methods=['POST'])
def add_task():
    """
    Обрабатывает добавление новой задачи
    
    Шаги:
    1. Валидация обязательных полей
    2. Проверка длины данных
    3. Парсинг даты/времени
    4. Сохранение в БД
    
    Возвращает:
    Перенаправление на главную страницу или ошибку
    """
    try:
        # Получение и очистка данных из формы
        title = request.form.get('title', '').strip()  # Обязательное поле
        description = request.form.get('description', '').strip()  # Обязательное поле
    except KeyError:
        abort(400, 'Обязательные поля: title, description')  # Если нет ключей формы
    
    # Проверка на пустые значения
    if not title or not description:
        abort(400, 'Поля не могут быть пустыми')
    
    # Проверка максимальной длины
    if len(title) > 50 or len(description) > 200:
        abort(400, "Превышена максимальная длина полей")
    
    # Обработка дедлайна
    deadline = None
    date_str = request.form.get('date')  # Необязательное поле
    time_str = request.form.get('time')  # Необязательное поле
    
    if date_str and time_str:
        try:
            # Парсинг строки в datetime-объект
            deadline_str = f'{date_str} {time_str}'
            deadline = datetime.strptime(deadline_str, '%d.%m.%Y %H:%M')
        except ValueError:
            abort(400, 'Некорректный формат даты/времени')

    # Создание и сохранение задачи
    new_task = Task(
        title=title,
        description=description,
        deadline=deadline,
        completed=False  # Значение по умолчанию
    )
    db.session.add(new_task)
    db.session.commit()
    
    return redirect(url_for('index'))  # Перенаправление на главную страницу

@tasks_bp.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@tasks_bp.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

@tasks_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        if date_str and time_str:
            deadline_str = f"{date_str} {time_str}"
            task.deadline = datetime.strptime(deadline_str, '%d.%m.%Y %H:%M')
        else:
            task.deadline = None
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', task=task)