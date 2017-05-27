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
        for level in app.config['LOG_LEVEL']:
            if level == 'INFO':
                handler.setLevel(logging.INFO)
            elif level == 'CRITICAL':
                handler.setLevel(logging.CRITICAL)
            elif level == 'DEBUG':
                handler.setLevel(logging.DEBUG)
            elif level == 'ERROR':
                handler.setLevel(logging.ERROR)
            elif level == 'FATAL':
                handler.setLevel(logging.FATAL)
            else:
                raise Exception('Invalid logging level')
    else:
        handler.setLevel(logging.INFO)
        print 'No "LOG_LEVEL" found defaulting to "INFO"'

    app.logger.addHandler(handler)

    return app
