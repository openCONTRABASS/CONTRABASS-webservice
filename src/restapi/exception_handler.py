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

import logging
import traceback

from flask import jsonify
from .exceptions import *

LOGGER = logging.getLogger(__name__)


def init_exception_handler(app):
    app.register_error_handler(ValidationException, handle_validation_exception)
    app.register_error_handler(NotFoundException, handle_not_found_exception)
    app.register_error_handler(DuplicateException, handle_duplicate_exception)
    app.register_error_handler(InvalidException, handle_invalid_exception)
    app.register_error_handler(Exception, handle_exception)


def handle_duplicate_exception(error):
    LOGGER.info(error)
    LOGGER.info("Response : 409")
    response = jsonify({"message": "Value already exists"})
    response.status_code = 409
    return response


def handle_validation_exception(error):
    LOGGER.info(error)
    LOGGER.info("Response : 400")
    response = jsonify({"message": str(error)})
    response.status_code = 400
    return response


def handle_not_found_exception(error):
    LOGGER.info(error)
    LOGGER.info("Response : 404")
    response = jsonify({"message": "Not found"})
    response.status_code = 404
    return response


def handle_exception(error):
    LOGGER.error(traceback.format_exc())
    LOGGER.info("Response : 500")
    response = jsonify({"message": "Internal server error"})
    response.status_code = 500
    return response


def handle_invalid_exception(error):
    LOGGER.info(error)
    LOGGER.info("Response : 401")
    response = jsonify({"message": str(error)})
    response.status_code = 401
    return response
