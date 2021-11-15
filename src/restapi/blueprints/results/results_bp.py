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
import itertools

from flask import Blueprint, jsonify
from celery.result import AsyncResult

from src.restapi.celery_app import (
    celery_app,
    get_pending_tasks_length,
    get_task_pending_position,
)

from src.restapi.service.ModelService import ModelService
from src.restapi.beans.ResponseChokepoints import *
from src.restapi.beans.Chokepoint import Chokepoint
from src.restapi.beans.ResponseReport import ResponseReport
from src.restapi.exceptions import InvalidException
from src.restapi.constants import RESPONSE_TASK_NONE


results_bp = Blueprint(
    "results_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)

LOGGER = logging.getLogger(__name__)

model_service = ModelService()

# Temporarily disabled
# @results_bp.route('/results/<uuid:uuid>/chokepoints', methods=['GET'])
def get_chokepoints(uuid):

    LOGGER.info(f"GET /results/{uuid}/chokepoints")

    uuid = str(uuid)
    result = ResponseChokepoints()

    async_result = AsyncResult(id=str(uuid), app=celery_app)
    result.status = async_result.state
    result.finished = async_result.ready()
    result.pending_length = get_task_pending_position(uuid)

    if async_result.ready():
        list_ob = []
        for r, m in async_result.get():
            list_ob.append(Chokepoint(r, m))
        result.result = list_ob
    else:
        result.result = []

    response = jsonify(vars(result))
    LOGGER.info(f"Response: {response}")
    return response


@results_bp.route("/results/<uuid:uuid>/critical_reactions", methods=["GET"])
def get_critical_reactions(uuid):

    LOGGER.info(f"GET /results/{uuid}/critical_reactions")

    uuid = str(uuid)
    result = ResponseReport()

    async_result = AsyncResult(id=str(uuid), app=celery_app)
    result.status = async_result.state
    result.finished = async_result.ready()
    result.pending_length = get_task_pending_position(uuid)

    if async_result.ready():
        try:
            output_path_html, output_path_spreadsheet = async_result.get()
            result.file_html = output_path_html
            result.file_spreadsheet = output_path_spreadsheet
        except Exception as err:
            raise InvalidException(traceback.print_exc())
    else:
        result.file_html = RESPONSE_TASK_NONE
        result.file_spreadsheet = RESPONSE_TASK_NONE

    response = jsonify(vars(result))
    LOGGER.info(f"Response: {response}")
    return response


@results_bp.route("/results/<uuid:uuid>/growth_dependent_reactions", methods=["GET"])
def get_growth_dependent_reactions(uuid):

    LOGGER.info(f"GET /results/{uuid}/growth_dependent_reactions")

    uuid = str(uuid)
    result = ResponseReport()

    async_result = AsyncResult(id=str(uuid), app=celery_app)
    result.status = async_result.state
    result.finished = async_result.ready()
    result.pending_length = get_task_pending_position(uuid)

    if async_result.ready():
        try:
            output_path_html, output_path_spreadsheet = async_result.get()
            result.file_html = output_path_html
            result.file_spreadsheet = output_path_spreadsheet
        except Exception as err:
            raise InvalidException(traceback.print_exc())
    else:
        result.file_html = RESPONSE_TASK_NONE
        result.file_spreadsheet = RESPONSE_TASK_NONE

    response = jsonify(vars(result))
    LOGGER.info(f"Response: {response}")
    return response


# Temporarily disabled
# @results_bp.route('/models/<uuid:uuid>/report_reactions', methods=['GET'])
def get_report_reactions(uuid):

    LOGGER.info(f"GET /models/{uuid}/report_reactions")

    uuid = str(uuid)
    result = ResponseReport()

    async_result = AsyncResult(id=str(uuid), app=celery_app)
    result.status = async_result.state
    result.finished = async_result.ready()
    result.pending_length = get_task_pending_position(uuid)

    if async_result.ready():
        try:
            result.result = async_result.get()
        except Exception as err:
            raise InvalidException(str(err))
    else:
        result.result = RESPONSE_TASK_NONE

    response = jsonify(vars(result))
    LOGGER.info(f"Response: {response}")
    return response


# Terminate a running task
@results_bp.route("/results/<uuid:uuid>/terminate", methods=["POST"])
def terminate_task(uuid):

    LOGGER.info(f"POST /results/{uuid}/terminate ")

    uuid = str(uuid)
    result = ResponseReport()

    async_result = AsyncResult(id=str(uuid), app=celery_app)
    async_result.revoke(signal="SIGKILL")

    LOGGER.info(f"Response: 'success':True 200")
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}
