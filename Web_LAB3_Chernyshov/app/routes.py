import random
from functools import lru_cache
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from faker import Faker
from . import app

fake = Faker('ru_RU')

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Конфигурация приложения
app.config['SECRET_KEY'] = 'your-secret-key'  # для работы с сессиями

# Простая модель пользователя
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# Словарь для хранения пользователей (в реальном приложении должна быть база данных)
users = {
    'admin': {'password': 'admin123'}
}

@login_manager.user_loader
def load_user(username):
    if username not in users:
        return None
    return User(username)

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = {
            'author': fake.name(),
            'text': fake.text()
        }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'title': 'Заголовок поста',
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }

@lru_cache
def posts_list():
    return sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('secret'))
        else:
            flash('Неверное имя пользователя или пароль')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

@app.route('/visits')
def visits():
    if 'visits' not in session:
        session['visits'] = 1
    else:
        session['visits'] = session['visits'] + 1
    return render_template('visits.html', visits=session['visits'])

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list())

@app.route('/posts/<int:index>')
def post(index):
    try:
        p = posts_list()[index]
        return render_template('post.html', title=p['title'], post=p)
    except IndexError:
        abort(404)

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

# ... остальные маршруты из app.py 