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
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    return app
