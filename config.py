"""
Configuration for Flask Application 'NKN Metadata Editor'
"""

import netCDF4
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    PRODUCTION = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    MONGODB_SETTINGS = {'db': 'scenarios'}

    BASE_PARAMETER_NC = netCDF4.Dataset('app/static/data/parameter.nc', 'r')


class TestingConfig(Config):
    TESTING = True

    MONGODB_SETTINGS = {'db': 'scenarios_test'}

    BASE_PARAMETER_NC = netCDF4.Dataset('test/data/parameter.nc', 'r')


class ProductionConfig(Config):
    PRODUCTION = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
