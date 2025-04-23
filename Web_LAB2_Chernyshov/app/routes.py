import random
from functools import lru_cache
from flask import render_template, abort, request, make_response, redirect, url_for
from faker import Faker
import re
from . import app

fake = Faker()

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.text() }
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

@app.route('/request-data/url-params')
def url_params():
    return render_template('request_data/url_params.html', 
                         title='Параметры URL',
                         params=request.args)

@app.route('/request-data/headers')
def headers():
    return render_template('request_data/headers.html',
                         title='Заголовки запроса',
                         headers=request.headers)

@app.route('/request-data/cookies')
def cookies():
    response = make_response(render_template('request_data/cookies.html',
                                           title='Cookie',
                                           cookies=request.cookies))
    
    if 'test_cookie' in request.cookies:
        response.delete_cookie('test_cookie')
    else:
        response.set_cookie('test_cookie', 'test_value', max_age=60*60*24)
    
    return response

@app.route('/request-data/form', methods=['GET', 'POST'])
def form_params():
    if request.method == 'POST':
        return render_template('request_data/form_params.html',
                             title='Параметры формы',
                             form_data=request.form)
    return render_template('request_data/form.html',
                         title='Форма')

@app.route('/phone-validation', methods=['GET', 'POST'])
def phone_validation():
    error = None
    formatted_number = None
    
    if request.method == 'POST':
        phone = request.form.get('phone', '')
        
        # Удаляем все допустимые символы, кроме цифр
        digits = re.sub(r'[+\s\(\)\-\.]', '', phone)
        
        # Проверяем наличие недопустимых символов
        if not re.match(r'^[\d\s\(\)\-\.\+]+$', phone):
            error = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
        # Проверяем количество цифр
        elif (phone.startswith('+7') or phone.startswith('8')) and len(digits) != 11:
            error = 'Недопустимый ввод. Неверное количество цифр.'
        elif not (phone.startswith('+7') or phone.startswith('8')) and len(digits) != 10:
            error = 'Недопустимый ввод. Неверное количество цифр.'
        else:
            # Форматируем номер
            if phone.startswith('+7'):
                digits = digits[1:]  # Убираем +7
            elif phone.startswith('8'):
                digits = digits[1:]  # Убираем 8
            
            formatted_number = f"8-{digits[:3]}-{digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
    
    return render_template('phone_validation.html',
                         title='Валидация номера телефона',
                         error=error,
                         formatted_number=formatted_number) 