#!/usr/bin/env python
from flask_script import Manager

from msa_stemmers import create_app

app = create_app(__name__)
manager = Manager(app)


@manager.command
def runserver(host='0.0.0.0', port=None):
    """Starts a lightweight development Web server on the local machine."""
    default_port = app.config['PORT']
    if host == 'localhost':
        host = '127.0.0.1'
    port = port if port else default_port
    app.run(debug=True, host=host, port=int(port))


@manager.option('-h', '--host', dest='host', default='')
@manager.option('-p', '--port', dest='port', type=int, default=0)
@manager.option('-w', '--workers', dest='workers', type=int, default=0)
def gunicorn(host, port, workers):
    from gunicorn.app.base import Application

    class FlaskApplication(Application):
        def init(self, parser, opts, args):
            cfg = self.get_config_from_module_name('gunicorn_release')
            clean_cfg = {}
            for k, v in cfg.items():
                # Ignore unknown names
                if k not in self.cfg.settings:
                    continue
                clean_cfg[k.lower()] = v

            if host:
                clean_cfg['host'] = host
            if port:
                clean_cfg['port'] = port
            if workers:
                clean_cfg['workers'] = workers
            return clean_cfg

        def load(self):
            return app

    application = FlaskApplication()
    return application.run()


if __name__ == '__main__':
    manager.run()
