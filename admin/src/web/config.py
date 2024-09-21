class Config(object):
    """Base configuracion. """
    
    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"


class ProductionConfig(Config):
    """Producton configuration."""
    
    pass


class DevelopmentConfig(Config):
    """Development configuration. """
    pass

class TestingConfig(Config):
    """Testing configuration. """

    TESTING = True

config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig
}