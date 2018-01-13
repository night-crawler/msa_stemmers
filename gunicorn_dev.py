import os

bind = '0.0.0.0:8000'
proc_name = 'stemmers'
workers = os.environ.get('GUNICORN_WORKERS', 2)
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'sync')
reload = True
preload_app = True
raw_env = [
    'LANG=ru_RU.UTF-8',
    'LC_ALL=ru_RU.UTF-8',
    'LC_LANG=ru_RU.UTF-8'
]
timeout = os.environ.get('GUNICORN_TIMEOUT', 10)
