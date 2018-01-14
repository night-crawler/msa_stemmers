import pytest

from msa_stemmers import create_app


@pytest.fixture('module')
def app():
    _app = create_app('testing', config_name='test')
    with _app.app_context():
        yield _app

