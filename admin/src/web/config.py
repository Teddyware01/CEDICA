from os import environ
import os

class Config(object):
    """Base configuracion."""

    SECRET_KEY = "secret"
    TESTING = True
    SESSION_TYPE = "filesystem"
    
    PAGINATION_PER_PAGE = 3


class ProductionConfig(Config):
    """Producton configuration."""
    MINIO_SERVER=environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")

    # Valores que pueden no tener en sus maquinas, pero que ya cargué en vault:
    OAUTH_GOOGLE_CLIENT_ID = environ.get('OAUTH_GOOGLE_CLIENT_ID')
    OAUTH_GOOGLE_CLIENT_SECRET = environ.get('OAUTH_GOOGLE_CLIENT_SECRET')
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'


class DevelopmentConfig(Config):
    """Development configuration."""
    # Config de Minio
    MINIO_SERVER="192.168.1.40:9000"
    MINIO_ACCESS_KEY = "crOnBZr4qHIukCC52lhY"
    MINIO_SECRET_KEY = "fZi5OKO0v0m0DKiRAEE23ZNTjXMMAIDAe2zRvkyS"
    MINIO_SECURE = False
    # Config de postgres
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo15"
    
    """
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    """
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://postgres:admin@localhost:5432/grupo15"
    )
    

    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'client_encoding': 'utf8'
        }
    }

    # Valores que pueden no tener en sus maquinas, pero que ya cargué en vault:
    OAUTH_GOOGLE_CLIENT_ID = environ.get('OAUTH_GOOGLE_CLIENT_ID')
    OAUTH_GOOGLE_CLIENT_SECRET = environ.get('OAUTH_GOOGLE_CLIENT_SECRET')
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
}
