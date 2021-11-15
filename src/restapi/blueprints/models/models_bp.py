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
import os

from flask import Blueprint, jsonify, current_app, request

from src.restapi.tasks.tasks import (
    compute_chokepoints_task,
    task_compute_critical_reactions,
    task_compute_growth_dependent_reactions,
)
from src.restapi.celery_app import celery_app, get_pending_tasks_length

from src.restapi.service.ModelService import ModelService
from src.restapi.beans.TaskInit import TaskInit
from src.restapi.beans.TaskFormCriticalReactions import TaskFormCriticalReactions
from src.restapi.beans.TaskFormReactionsSets import TaskFormReactionsSets
from src.restapi.beans.ConfigReactionsSets import ConfigReactionsSets
from src.restapi.beans.OptimizationEnum import OptimizationEnum
from src.restapi.beans.MediumEnum import MediumEnum
from src.restapi.validation import sanitize_string, empty_string


models_bp = Blueprint(
    "models_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)

LOGGER = logging.getLogger(__name__)

model_service = ModelService()

# Temporarily disabled
# @models_bp.route('/models/<uuid:uuid>/chokepoints', methods=['POST'])
def compute_chokepoints(uuid):

    LOGGER.info(f"POST /models/{uuid}/chokepoints")

    sanitize_string(str(uuid))

    filename = model_service.query_by_uuid(uuid).url
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    task = compute_chokepoints_task.delay(path)
    task_uuid = task.id

    response = jsonify(vars(TaskInit(task_uuid, get_pending_tasks_length())))
    LOGGER.info(f"Response: {response}")
    return response


@models_bp.route("/models/<uuid:uuid>/critical_reactions", methods=["POST"])
def compute_critical_reactions(uuid):

    request_data = request.form
    print(f"POST /models/{uuid}/critical_reactions {request_data}")

    objective = None
    fraction_of_optimum = None

    sanitize_string(str(uuid))

    form = TaskFormCriticalReactions(request.form)
    if not form.validate():
        raise ValidationException("Incorrect data")

    if not empty_string(form.objective.data):
        sanitize_string(form.objective.data)
        objective = str(form.objective.data)

    if form.fraction_of_optimum.data is not None:
        fraction_of_optimum = float(form.fraction_of_optimum.data)

    filename = model_service.query_by_uuid(uuid).url
    pathname = current_app.config["UPLOAD_FOLDER"]
    path = os.path.join(pathname, filename)
    output_dir = current_app.config["STATIC_FOLDER"]
    output_filename = str(uuid) + current_app.config["OUTPUT_FILE_EXTENSION"]

    task = task_compute_critical_reactions.delay(
        path,  # model path
        output_dir + "/" + output_filename,  # output path
        objective=objective,
        fraction_of_optimum=fraction_of_optimum,
        model_uuid=str(uuid),
    )
    task_uuid = task.id

    response = jsonify(vars(TaskInit(task_uuid, get_pending_tasks_length())))
    LOGGER.info(f"Response: {response}")
    return response


@models_bp.route("/models/<uuid:uuid>/growth_dependent_reactions", methods=["POST"])
def compute_growth_dependent_reactions(uuid):

    request_data = request.form
    LOGGER.info(f"POST /models/{uuid}/growth_dependent_reactions {request_data}")

    objective = None

    sanitize_string(str(uuid))

    form = TaskFormCriticalReactions(request.form)
    if not form.validate():
        raise ValidationException("Incorrect data")

    if not empty_string(form.objective.data):
        sanitize_string(form.objective.data)
        objective = str(form.objective.data)

    filename = model_service.query_by_uuid(uuid).url
    pathname = current_app.config["UPLOAD_FOLDER"]
    path = os.path.join(pathname, filename)
    output_dir = current_app.config["STATIC_FOLDER"]
    output_filename = str(uuid) + current_app.config["OUTPUT_FILE_EXTENSION"]

    task = task_compute_growth_dependent_reactions.delay(
        path, output_dir + "/" + output_filename, objective, str(uuid)  # output path
    )
    task_uuid = task.id

    response = jsonify(vars(TaskInit(task_uuid, get_pending_tasks_length())))
    LOGGER.info(f"Response: {response}")
    return response


# Temporarily disabled
# @models_bp.route('/models/<uuid:uuid>/report_reactions', methods=['POST'])
def compute_report_reactions(uuid):

    request_data = request.form
    LOGGER.info(f"POST /models/{uuid}/report_reactions {request_data}")

    objective = None
    fraction_of_optimum = None
    medium = MediumEnum.DEFAULT
    optimization = OptimizationEnum.FBA
    skip_knockout = True

    form = TaskFormReactionsSets(request.form)
    if not form.validate():
        raise ValidationException("Datos Incorrectos")
    sanitize_string(form.objective.data)
    sanitize_string(str(uuid))

    if not empty_string(form.objective.data):
        objective = str(form.objective.data)
    if form.fraction_of_optimum.data is not None:
        fraction_of_optimum = float(form.fraction_of_optimum.data)
    if form.medium.data is not None:
        medium = MediumEnum[str(form.medium.data)]
    if form.optimization.data is not None:
        optimization = OptimizationEnum[str(form.optimization.data)]
    if form.skip_knockout.data is not None:
        print(form.skip_knockout.data)
        skip_knockout = bool(form.skip_knockout.data)

    filename = model_service.query_by_uuid(uuid).url
    pathname = current_app.config["UPLOAD_FOLDER"]
    path = os.path.join(pathname, filename)
    output_dir = current_app.config["STATIC_FOLDER"]
    output_filename = str(uuid) + current_app.config["OUTPUT_FILE_EXTENSION"]

    config = ConfigReactionsSets()
    config.fraction_of_optimum = fraction_of_optimum
    config.objective = objective
    config.medium = medium
    config.optimization = optimization
    config.skip_knockout_computation = skip_knockout

    task = compute_sets_report_task.delay(
        path, output_dir, output_filename, str(uuid), config
    )
    task_uuid = task.id

    response = jsonify(vars(TaskInit(task_uuid, get_pending_tasks_length())))
    LOGGER.info(f"Response: {response}")
    return response
