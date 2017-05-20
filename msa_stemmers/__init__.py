from flask import Flask
from flask_jsonrpc import JSONRPC

__version__ = '0.0.0'

# global, but you can make it better =) (for instance: app.jsonrpc etc)
jsonrpc = JSONRPC(service_url='/api', enable_web_browsable_api=True)


def create_app(import_name: str, config_name: str='default') -> Flask:
    from .config import configure_app  # noqa
    from . import views  # noqa

    app = Flask(import_name)

    # configuration
    configure_app(app, config_name=config_name)

    # initialization
    jsonrpc.init_app(app)

    return app
