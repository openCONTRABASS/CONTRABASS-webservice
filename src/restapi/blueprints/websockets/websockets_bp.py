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

from flask import Blueprint, jsonify, current_app

from src.restapi.service.ModelService import ModelService
from src.restapi.beans.ResponseChannel import *
from src.restapi.beans.ResponseEndpoint import *
from src.restapi.beans.WebsocketEvent import *
from src.restapi.exceptions import *
from src.restapi.constants import *
from src.restapi.validation import *

websockets_bp = Blueprint(
    "websockets_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)

LOGGER = logging.getLogger(__name__)

model_service = ModelService()


@websockets_bp.route("/websockets/get_endpoint", methods=["GET"])
def get_endpoint():

    LOGGER.info(f"GET /websockets/get_endpoint")

    result = ResponseEndpoint(current_app.config["WEBSOCKETS_URL"])

    response = jsonify(vars(result))
    LOGGER.info(f"Response: {response}")
    return response


@websockets_bp.route("/websockets/notification_channel/<uuid:uuid>", methods=["GET"])
def get_notification_channel(uuid):

    LOGGER.info(f"GET /websockets/notification_channel/{uuid}")

    uuid = str(uuid)
    sanitize_string(uuid)

    # validate submit exists
    model_bd = model_service.query_by_uuid(uuid)

    result = ResponseChannel(model_bd.uuid)

    response = jsonify(vars(result))
    LOGGER.info(f"Response: {response}")
    return response


@websockets_bp.route("/websockets/example_event_join", methods=["GET"])
def get_example_join_event():

    LOGGER.info(f"GET /websockets/example_event_join")

    result = WebsocketEvent("join", "00000000-0000-0000-0000-000000000000")

    response = jsonify(vars(result))
    LOGGER.info(f"Response: {response}")
    return response


@websockets_bp.route("/websockets/example_event_message", methods=["GET"])
def get_example_event_message():

    LOGGER.info(f"GET /websockets/example_event_message")

    result = WebsocketEvent(
        "00000000-0000-0000-0000-000000000000", "<<message-content>>"
    )

    response = jsonify(vars(result))
    LOGGER.info(f"Response: {response}")
    return response
