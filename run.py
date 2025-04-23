from wsgiref.simple_server import make_server
from wsgi import application

if __name__ == '__main__':
    # Создаем сервер на localhost:8000
    with make_server('', 8000, application) as httpd:
        print("Сервер запущен на http://localhost:8000")
        print("Нажмите Ctrl+C для остановки сервера")
        # Запускаем сервер
        httpd.serve_forever() 