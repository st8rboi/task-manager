from flask import Flask, render_template, request, Blueprint, redirect, url_for, abort
from extensions import db
from models import Task
from datetime import datetime
from validators import validate_required_fields, validate_length
from flask_login import login_required, current_user

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/add', methods=['POST'])
@login_required
def add_task():
    form_data = {
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip()       
    }
    validate_required_fields(form_data, ['title', 'description'])
    validate_length(form_data, {'title': 50, 'description': 200})

    deadline = None
    date_str = request.form.get('date')
    time_str = request.form.get('time')

    if date_str and time_str:
        try:
            deadline_str = f'{date_str} {time_str}'
            deadline = datetime.strptime(deadline_str, '%d.%m.%Y %H:%M')
        except ValueError:
            abort(400, 'Некорректный формат даты/времени')

    new_task = Task(
        title=form_data['title'],
        description=form_data['description'],
        deadline=deadline,
        completed=False,
        user_id=current_user.id
    )
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))

@tasks_bp.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@tasks_bp.route('/complete/<int:id>')
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        abort(403)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

@tasks_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        if date_str and time_str:
            try:
                deadline_str = f"{date_str} {time_str}"
                task.deadline = datetime.strptime(deadline_str, '%d.%m.%Y %H:%M')
            except ValueError:
                abort(400, 'Некорректный формат даты/времени')
        else:
            task.deadline = None

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update.html', task=task)
