class Config(object):
    DEBUG = False
    TESTING = False
    LOG_FILENAME = 'wol.log'
    LOG_MAX_BYTES = 10000
    LOG_BACKUP_COUNT = 1


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
