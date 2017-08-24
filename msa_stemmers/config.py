import os


class BaseConfig:
    CONFIG_FILE = os.path.abspath(__file__)
    CONFIG_DIR = os.path.dirname(CONFIG_FILE)
    BASE_DIR = os.path.abspath(os.path.join(CONFIG_DIR, '..'))

    DEBUG = False
    TESTING = False
    HOST = 'localhost'
    PORT = 8000


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True


config = {
    'default': 'msa_stemmers.config.DevelopmentConfig',
    'dev': 'msa_stemmers.config.DevelopmentConfig',
    'prod': 'msa_stemmers.config.ProductionConfig',
    'test': 'msa_stemmers.config.TestingConfig',
}


def configure_app(app, config_name='default'):
    config_name = os.getenv('MSA_STEMMERS_CONFIG_NAME', None) or config_name

    app.config.from_object(config[config_name])
    app.config.from_envvar('MSA_STEMMERS', silent=True)
