class Config:
    THEME = 'reactor'
    THEMES = ['reactor', 'station']


class DevelopmentConfig(Config):
    ENV = 'development'
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    ENV = 'production'
    TESTING = False
    DEBUG = False
