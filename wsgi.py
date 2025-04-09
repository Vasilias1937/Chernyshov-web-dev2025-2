import sys
import os

# Добавляем пути к приложениям в sys.path
path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)

# Импортируем приложения
from Web_LAB1_Chernyshov.app.app import app as lab1_app
from Web_LAB2_Chernyshov.app.app import app as lab2_app

# Создаем словарь приложений
applications = {
    '/lab1': lab1_app,
    '/lab2': lab2_app
}

def application(environ, start_response):
    # Получаем путь запроса
    path = environ.get('PATH_INFO', '')
    
    # Определяем, какое приложение должно обработать запрос
    for prefix, app in applications.items():
        if path.startswith(prefix):
            # Удаляем префикс из пути для правильной маршрутизации внутри приложения
            environ['PATH_INFO'] = path[len(prefix):]
            return app(environ, start_response)
    
    # Если путь не соответствует ни одному приложению, возвращаем 404
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'Not Found'] 