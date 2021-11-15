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

from src.restapi.celery_app import celery_app
from src.restapi.util.model_utils import *
from src.restapi.util.report_utils import *
from src.restapi.util.report_sets_utils import *


# Example task
@celery_app.task
def compute_chokepoints_task(model_path, exclude_dead_reactions=True):
    return compute_chokepoints(model_path, exclude_dead_reactions)


@celery_app.task
def compute_sets_report_task(
    model_path, output_path, output_filename, model_uuid, config
):
    generate_sets_report(
        model_path, output_path + "/" + output_filename, model_uuid, config
    )
    return output_filename


@celery_app.task
def task_compute_critical_reactions(
    model_path, output_path, objective=None, fraction_of_optimum=None, model_uuid=None
):
    return compute_critical_reactions(
        model_path, output_path, objective, fraction_of_optimum, model_uuid
    )


@celery_app.task
def task_compute_growth_dependent_reactions(
    model_path, output_path, objective=None, model_uuid=None
):
    return compute_growth_dependent_reactions(
        model_path, output_path, objective, model_uuid
    )
