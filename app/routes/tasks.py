# Импорт необходимых модулей
from flask import Flask, render_template, request, Blueprint, redirect, url_for, abort
from extensions import db  # Импорт объекта SQLAlchemy для работы с БД
from models import Task  # Модель задачи из БД
from datetime import datetime  # Для работы с датой/временем
from validators import validate_required_fields, validate_length

# Создание Blueprint для группировки маршрутов, связанных с задачами
tasks_bp = Blueprint('tasks', __name__)

# Маршрут: Добавление задачи (POST-запрос)
@tasks_bp.route('/add', methods=['POST'])
def add_task():
    """
    Обрабатывает добавление новой задачи через форму.

    Параметры формы:
    - title (обязательный): Название задачи (макс. 50 символов)
    - description (обязательный): Описание задачи (макс. 200 символов)
    - date (необязательный): Дата в формате DD.MM.YYYY
    - time (необязательный): Время в формате HH:MM

    Возвращает:
    - Перенаправление на главную страницу при успехе.
    - Ошибку 400 при некорректных данных.
    """
    # Получение данных из формы с удалением пробелов по краям
    form_data = {
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip()       
    }
    validate_required_fields(form_data, ['title', 'description'])
    validate_length(form_data, {'title': 50, 'description': 200})

    # Парсинг даты и времени (необязательные поля)
    deadline = None
    date_str = request.form.get('date')
    time_str = request.form.get('time')

    if date_str and time_str:
        try:
            # Сборка строки даты-времени и преобразование в объект datetime
            deadline_str = f'{date_str} {time_str}'
            deadline = datetime.strptime(deadline_str, '%d.%m.%Y %H:%M')
        except ValueError:
            abort(400, 'Некорректный формат даты/времени')  # Ошибка парсинга

    # Создание объекта задачи и сохранение в БД
    new_task = Task(
        title=form_data['title'],
        description=form_data['description'],
        deadline=deadline,
        completed=False
    )
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))  # Перенаправление на главную

# Маршрут: Удаление задачи (GET-запрос)
@tasks_bp.route('/delete/<int:id>')
def delete_task(id):
    """
    Удаляет задачу по ID.

    Параметры URL:
    - id (int): Уникальный идентификатор задачи.

    Возвращает:
    - Перенаправление на главную страницу.
    - Ошибку 404, если задача не найдена.
    """
    task = Task.query.get_or_404(id)  # Поиск задачи или 404
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

# Маршрут: Переключение статуса задачи (GET-запрос)
@tasks_bp.route('/complete/<int:id>')
def complete_task(id):
    """
    Меняет статус выполнения задачи на противоположный.

    Параметры URL:
    - id (int): Уникальный идентификатор задачи.

    Возвращает:
    - Перенаправление на главную страницу.
    - Ошибку 404, если задача не найдена.
    """
    task = Task.query.get_or_404(id)
    task.completed = not task.completed  # Инверсия статуса
    db.session.commit()
    return redirect(url_for('index'))

# Маршрут: Редактирование задачи (GET и POST)
@tasks_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    """
    Редактирует существующую задачу.

    Параметры URL:
    - id (int): Уникальный идентификатор задачи.

    GET: Отображает форму редактирования.
    POST: Обновляет данные задачи.

    Возвращает:
    - HTML-форму при GET.
    - Перенаправление на главную при POST.
    - Ошибку 404, если задача не найдена.
    """
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        # Обновление данных из формы
        task.title = request.form['title']
        task.description = request.form['description']
        
        # Обновление дедлайна
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        if date_str and time_str:
            deadline_str = f"{date_str} {time_str}"
            task.deadline = datetime.strptime(deadline_str, '%d.%m.%Y %H:%M')
        else:
            task.deadline = None  # Сброс дедлайна

        db.session.commit()
        return redirect(url_for('index'))

    # Отображение формы редактирования с текущими данными задачи
    return render_template('update.html', task=task)