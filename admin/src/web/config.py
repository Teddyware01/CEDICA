from os import environ
import os

class Config(object):
    """Base configuracion."""

    SECRET_KEY = "secret"
    TESTING = True
    SESSION_TYPE = "filesystem"


class ProductionConfig(Config):
    """Producton configuration."""
    MINIO_SERVER=environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    

class DevelopmentConfig(Config):
    """Development configuration."""
    # Config de Minio
    MINIO_SERVER="192.168.1.40:9000"
    MINIO_ACCESS_KEY = "LKzNI6N4wuR6xDHJ9BBc"
    MINIO_SECRET_KEY = "hmMvq5msVThLa7Gy3hud0h5kahkU2qnAJNAmgGnj"
    MINIO_SECURE = False
    # Config de postgres
    DB_USER = "postgres"
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo15"
    
    """
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    """
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://postgres:postgres@localhost:5432/grupo15"
    )
    
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'client_encoding': 'utf8'
        }
    }
    
    
    


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
}
