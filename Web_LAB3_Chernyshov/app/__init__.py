import logging
from flask import Flask

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    filename='app.log'
)

from . import routes  # импортируем маршруты из routes.py 