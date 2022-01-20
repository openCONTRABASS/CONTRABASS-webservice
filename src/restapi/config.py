"""
    This file is part of CONTRABASS-webservice project.
    Copyright (C) 2020-2021  Alex Oarga  <718123 at unizar dot es> (University of Zaragoza)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    DEBUG = True
    TESTING = False

    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")

    OUTPUT_FILE_EXTENSION = ".xls"

    MAX_CONTENT_LENGTH = 1024 * 1024 * 30  # 30MB max file size

    DICT_LOGGER = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": ("%(asctime)s [%(levelname)s] [%(name)s] | %(message)s")
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": True,
        },
    }


class ProductionConfig(Config):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql:"
        + f"//{os.environ.get('MYSQL_USER')}:"
        + f"{os.environ.get('MYSQL_PASSWORD')}"
        + f"@{os.environ.get('MYSQL_HOST')}"
        f"/{os.environ.get('MYSQL_DATABASE')}"
    )
    SQLALCHEMY_POOL_SIZE = 1

    CELERY_IMPORTS = "app"
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
    REDIS_BROKER_URL = os.environ.get("REDIS_BROKER_URL")
    WEBSOCKETS_URL = os.environ.get("WEBSOCKETS_URL")

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
    STATIC_FOLDER = os.environ.get("STATIC_FOLDER")

    DICT_LOGGER = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": ("%(asctime)s [%(levelname)s] [%(name)s] | %(message)s")
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": True,
        },
    }


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql:"
        + f"//{os.environ.get('MYSQL_USER')}:"
        + f"{os.environ.get('MYSQL_PASSWORD')}"
        + f"@{os.environ.get('MYSQL_HOST')}"
        f"/{os.environ.get('MYSQL_DATABASE')}"
    )
    SQLALCHEMY_POOL_SIZE = 1

    CELERY_IMPORTS = "app"
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
    REDIS_BROKER_URL = "redis://localhost:6379"
    WEBSOCKETS_URL = "localhost:5000"

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
    STATIC_FOLDER = os.environ.get("STATIC_FOLDER")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql:"
        + f"//{os.environ.get('MYSQL_USER')}:"
        + f"{os.environ.get('MYSQL_PASSWORD')}"
        + f"@{os.environ.get('MYSQL_HOST')}"
        f"/{os.environ.get('MYSQL_DATABASE')}"
    )
    SQLALCHEMY_POOL_SIZE = 1

    CELERY_IMPORTS = "app"
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"
    REDIS_BROKER_URL = "redis://localhost:6379"
    WEBSOCKETS_URL = "localhost:5000"

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")
    STATIC_FOLDER = os.environ.get("STATIC_FOLDER")


class TestingConfig(Config):
    TESTING = True
    """
    If DEBUG is set to True it causes an AssertionError. See:
    - https://github.com/ga4gh/ga4gh-server/issues/791
    - https://github.com/alexmclarty/mirror/issues/6
    """
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_POOL_SIZE = None
    SQLALCHEMY_POOL_TIMEOUT = None

    CELERY_IMPORTS = "app"
    CELERY_BROKER_URL = "redis://"
    CELERY_RESULT_BACKEND = "redis://"
    REDIS_BROKER_URL = "redis://"
    WEBSOCKETS_URL = "localhost:5000"

    UPLOAD_FOLDER = "/tmp"
    STATIC_FOLDER = "/tmp"
