import os

bind = '0.0.0.0:8000'
workers = os.environ.get('GUNICORN_WORKERS', 4)
reload = True
preload_app = True
raw_env = [
    'LANG=ru_RU.UTF-8',
    'LC_ALL=ru_RU.UTF-8',
    'LC_LANG=ru_RU.UTF-8'
]
timeout = os.environ.get('GUNICORN_TIMEOUT', 10)
