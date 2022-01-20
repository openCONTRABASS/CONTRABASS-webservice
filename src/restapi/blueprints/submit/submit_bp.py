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

import uuid
import os
import logging
from urllib.request import urlopen
import requests

from cobra.io.sbml import CobraSBMLError
from flask import Blueprint, jsonify, current_app, request
from celery.result import AsyncResult

from src.restapi.celery_app import celery_app
from src.restapi.service.ModelService import ModelService
from src.restapi.validation import *
from src.restapi.util.model_utils import read_model, read_model_url, ordered_reactions_list
from src.restapi.beans.ModelId import ModelId
from src.restapi.beans.SubmitURL import SubmitURL

from werkzeug.utils import secure_filename

submit_bp = Blueprint(
    "submit_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)

LOGGER = logging.getLogger(__name__)

XML_EXTENSION = ".xml"

model_service = ModelService()


@submit_bp.route("/submit", methods=["POST"])
def submit_model():

    LOGGER.info("POST /submit")

    if "file" not in request.files:
        raise ValidationException("No file part")

    file = request.files["file"]
    if file.filename == "":
        raise ValidationException("No selected file")

    if not (file and allowed_file(file.filename)):
        raise ValidationException("Invalid file extension")

    filename, file_extension = os.path.splitext(secure_filename(file.filename))
    model_uuid = str(uuid.uuid4())
    filename = f"{model_uuid}{file_extension}"

    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    LOGGER.info(f"Saving model to: {filename}")
    file.save(path)

    # check submit for errors
    cobra_model = None
    try:
        LOGGER.info(f"Reading model ... : {filename}")
        cobra_model = read_model(path)
        LOGGER.info(f"Reading model DONE : {filename}")
    except CobraSBMLError as error:
        os.remove(path)
        raise ValidationException(str(error))

    model_service.insert(model_uuid, filename)

    response = ModelId(
        model_uuid,
        len(cobra_model.metabolites),
        len(cobra_model.reactions),
        len(cobra_model.genes),
        ordered_reactions_list(cobra_model)
    ).__dict__
    LOGGER.info(f"Response: {response}")
    return jsonify(response)


@submit_bp.route("/submit_url", methods=["POST"])
def submit_model_url():

    LOGGER.info("POST /submit_url")

    form = SubmitURL(request.form)
    if not form.validate():
        raise ValidationException("Incorrect data")

    LOGGER.info(f"POST /submit_url {request.form}")

    # The model is checked first to check its a valid model.
    file = requests.get(form.model_url.data)
    model_string = file.text

    try:
        LOGGER.info(f"Reading model from URL ")
        cobra_model = read_model_url(model_string)
        LOGGER.info(f"Reading model DONE URL done")
    except CobraSBMLError as error:
        raise ValidationException(str(error))

    # If we reach here the model is valid and we can save it
    model_uuid = str(uuid.uuid4())
    filename = f"{model_uuid}{XML_EXTENSION}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    LOGGER.info(f"Saving model to: {filename}")

    # Save file data to local copy
    with open(path, "w") as text_file:
        text_file.write(model_string)

    model_service.insert(model_uuid, filename)

    response = ModelId(
        model_uuid,
        len(cobra_model.metabolites),
        len(cobra_model.reactions),
        len(cobra_model.genes),
        ordered_reactions_list(cobra_model)
    ).__dict__
    LOGGER.info(f"Response: {response}")
    return jsonify(response)
