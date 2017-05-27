#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
import logging
from logging.handlers import RotatingFileHandler


def create_app(name, config='config.ProductionConfig'):
    app = Flask(name)
    app.config.from_object(config)

    handler = RotatingFileHandler(
        app.config['LOG_FILENAME'],
        maxBytes=app.config['LOG_MAX_BYTES'],
        backupCount=app.config['LOG_BACKUP_COUNT']
    )

    if 'LOG_LEVEL' in app.config:
        if app.config['LOG_LEVEL'] == 'INFO':
            handler.setLevel(logging.INFO)
        elif app.config['LOG_LEVEL'] == 'CRITICAL':
            handler.setLevel(logging.CRITICAL)
        elif app.config['LOG_LEVEL'] == 'DEBUG':
            handler.setLevel(logging.DEBUG)
        elif app.config['LOG_LEVEL'] == 'ERROR':
            handler.setLevel(logging.ERROR)
        elif app.config['LOG_LEVEL'] == 'FATAL':
            handler.setLevel(logging.FATAL)
        else:
            handler.setLevel(logging.INFO)
            print 'No "LOG_LEVEL" found defaulting to "INFO"'
    else:
        handler.setLevel(logging.INFO)
        print 'No "LOG_LEVEL" found defaulting to "INFO"'

    app.logger.addHandler(handler)

    return app
