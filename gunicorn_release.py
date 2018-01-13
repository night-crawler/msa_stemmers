import os

bind = '0.0.0.0:8000'
workers = os.environ.get('GUNICORN_WORKERS', 8)
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'sync')
pid = '/application/run/gunicorn.pid'
reload = True
preload_app = True
chdir = '/application/msa_stemmers/'
raw_env = [
    'LANG=ru_RU.UTF-8',
    'LC_ALL=ru_RU.UTF-8',
    'LC_LANG=ru_RU.UTF-8'
]
user = 'msa_stemmers'
group = 'msa_stemmers'
timeout = os.environ.get('GUNICORN_TIMEOUT', 10)
