import pytest

from msa_stemmers import create_app


@pytest.fixture('module')
def app():
    _app = create_app('testing', config_name='test')
    with _app.app_context():
        yield _app


@pytest.fixture('module')
def server(app):
    from flask_jsonrpc.proxy import ServiceProxy

    service_url = 'http://{host}:{port}/api'.format(
        host=app.config['HOST'],
        port=app.config['PORT'],
    )
    return ServiceProxy(service_url)
