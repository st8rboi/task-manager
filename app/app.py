from flask import Flask, render_template, redirect, url_for
from models import Task, User
from extensions import init_extensions, db, login_manager
from datetime import datetime
from routes.tasks import tasks_bp 
from routes.auth import auth_bp
from flask_login import current_user
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, '..', 'templates')

app = Flask(__name__, template_folder=TEMPLATES_DIR)

# Конфигурация из переменных окружения
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '23wesdxc')

# Инициализация расширений
init_extensions(app)

# Регистрация blueprints
app.register_blueprint(tasks_bp)
app.register_blueprint(auth_bp)

# Загрузка пользователя для Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница с фильтрацией задач

@app.route('/')
@app.route('/<filter>')
def index(filter='all'):
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))  # auth — это имя blueprint

    match filter:
        case 'completed':
            tasks = Task.query.filter_by(user_id=current_user.id, completed=True).all()
        case 'pending':
            tasks = Task.query.filter_by(user_id=current_user.id, completed=False).all()
        case _:
            tasks = Task.query.filter_by(user_id=current_user.id).all()

    return render_template('index.html', tasks=tasks)

# Точка входа
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
