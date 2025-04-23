from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Замените на реальный секретный ключ
app.config['APPLICATION_ROOT'] = '/lab3'
app.config['SERVER_NAME'] = 'localhost:8000'
app.config['URL_PREFIX'] = '/lab3'
app.config['SCRIPT_NAME'] = '/lab3'

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице необходимо авторизоваться'

# Модель пользователя
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Загрузчик пользователя
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница счетчика посещений
@app.route('/visits')
def visits():
    if 'visits' not in session:
        session['visits'] = 0
    session['visits'] += 1
    return render_template('visits.html', visits=session['visits'])

# Страница входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if username == 'user' and password == 'qwerty':
            user = User(username)
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('login.html')

# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

# Секретная страница
@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

if __name__ == '__main__':
    app.run(debug=True) 