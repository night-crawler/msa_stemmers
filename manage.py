#!/usr/bin/env python
import os
import sys
from setproctitle import setproctitle

import nltk
from flask_script import Manager

from msa_stemmers import create_app
from msa_stemmers.utils import ensure_nltk_ready

app = create_app('stemmers')
manager = Manager(app)
setproctitle('stemmers')

if hasattr(sys, 'pypy_version_info'):
    sys.stdout.write('RUNNING IN PYPY %s!\n' % str(sys.pypy_version_info))
    sys.stdout.flush()


@manager.command
def runserver(host='0.0.0.0', port=None):
    """Starts a lightweight development Web server on the local machine."""
    default_port = app.config['PORT']
    if host == 'localhost':
        host = '127.0.0.1'
    port = port if port else default_port
    app.run(debug=True, host=host, port=int(port))


@manager.command
def gunicorn():
    ensure_nltk_ready()
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            module_name = os.environ.get('GUNICORN_MODULE', 'gunicorn_dev')
            cfg = self.get_config_from_module_name(module_name)
            clean_cfg = {}
            for k, v in cfg.items():
                # Ignore unknown names
                if k not in self.cfg.settings:
                    continue
                clean_cfg[k.lower()] = v
            return clean_cfg

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()


@manager.option('-h', '--host', dest='host')
@manager.option('-p', '--port', dest='port')
def uwsgi(host=None, port=None):
    ensure_nltk_ready()
    from uwsgi_env.utils import uwsgi as _uwsgi
    return _uwsgi(host=host, port=port, project='msa_stemmers')


@manager.option('-h', '--host', dest='host')
@manager.option('-p', '--port', dest='port')
def bjoern(host=None, port=None):
    import bjoern as bj
    host = host or os.getenv('HOST', '0.0.0.0')
    port = int(port or os.getenv('PORT', port) or '8000')
    return bj.run(app, host, port, reuse_port=True)


@manager.command
def download_nltk():
    nltk.download('stopwords')


if __name__ == '__main__':
    manager.run()
