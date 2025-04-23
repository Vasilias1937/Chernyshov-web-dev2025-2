import sys
import os

# Добавляем пути к приложениям в sys.path
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)

# Импортируем приложения
from Web_LAB1_Chernyshov.app import app as lab1_app
from Web_LAB2_Chernyshov.app import app as lab2_app
from Web_LAB3_Chernyshov.app import app as lab3_app

# Создаем словарь приложений
applications = {
    '/lab1': lab1_app,
    '/lab2': lab2_app,
    '/lab3': lab3_app
}

def serve_static_file(file_path, start_response):
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [content]
    except FileNotFoundError:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']

def application(environ, start_response):
    # Получаем путь запроса
    path = environ.get('PATH_INFO', '')
    print(f"Получен запрос: {path}")  # Отладочная информация
    
    # Обработка главной страницы
    if path == '/' or path == '/index.html':
        return serve_static_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), start_response)
    
    # Определяем, какое приложение должно обработать запрос
    for prefix, app in applications.items():
        if path.startswith(prefix):
            print(f"Обработка запроса для {prefix}")  # Отладочная информация
            # Удаляем префикс из пути для правильной маршрутизации внутри приложения
            environ['SCRIPT_NAME'] = prefix
            environ['PATH_INFO'] = path[len(prefix):] or '/'
            print(f"PATH_INFO: {environ['PATH_INFO']}")  # Отладочная информация
            
            # Устанавливаем переменные окружения для Flask
            environ['wsgi.url_scheme'] = 'https' if environ.get('HTTP_X_FORWARDED_PROTO') == 'https' else 'http'
            environ['SERVER_NAME'] = environ.get('HTTP_HOST', 'localhost')
            environ['SERVER_PORT'] = environ.get('SERVER_PORT', '8000')
            
            try:
                return app(environ, start_response)
            except Exception as e:
                print(f"Ошибка при обработке запроса: {str(e)}")  # Отладочная информация
                start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
                return [str(e).encode()]
    
    # Если путь не соответствует ни одному приложению, возвращаем 404
    print(f"Путь не найден: {path}")  # Отладочная информация
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'Not Found'] 