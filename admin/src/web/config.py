from os import environ

class Config(object):
    """Base configuracion. """
    
    SECRET_KEY = "secret"
    TESTING = True ## luego cambiar, puede ser un error al levantar el programa
    SESSION_TYPE = "filesystem"


class ProductionConfig(Config):
    """Producton configuration."""
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    

class DevelopmentConfig(Config):
    """Development configuration. """
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo15"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )   
    SQLALCHEMY_TRACK_MODIFICATIONS = False  ##sacar esto
    

class TestingConfig(Config):
    """Testing configuration. """

    TESTING = True

config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig
}