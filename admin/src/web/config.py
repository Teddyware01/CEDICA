from os import environ
import os

class Config(object):
    """Base configuracion."""

    SECRET_KEY = "secret"
    TESTING = False
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
    MINIO_SERVER="127.0.1:9000"
    MINIO_ACCESS_KEY = "t72c7MVDNIvv686yDHkm"
    MINIO_SECRET_KEY = "CiYoF08qw3jB8fXcYkC9wZDj51KqSzIW2U8eg8F0"
    MINIO_SECURE = False
    # Config de postgres
    DB_USER = "postgres"
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo15"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
}
