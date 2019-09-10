class Config:
    pass


class DevelopmentConfig(Config):
    ENV = 'development'
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    ENV = 'production'
    TESTING = False
    DEBUG = False
