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
import ntpath

from celery.utils.log import get_task_logger
from contrabass.core import Facade
from contrabass.core import FacadeUtils
from contrabass.core.utils.CriticalCPConfig import CriticalCPConfig
from contrabass.core.utils.GrowthDependentCPConfig import GrowthDependentCPConfig

from src.restapi.socket_util import send_message_client

LOGGER = get_task_logger(__name__)

def compute_critical_reactions(model_path, output_path, objective=None, fraction_of_optimum=None, model_uuid=None):

    def verbose_f(text, args1=None, args2=None):
        '''
        args1 = ws room name
        args2 = None
        '''
        LOGGER.info(text)
        send_message_client(args1, text)

    config = CriticalCPConfig()
    config.model_path = model_path
    config.print_f = verbose_f
    config.args1 = model_uuid  # this is the ws room identifier
    config.args2 = None
    config.output_path_spreadsheet = output_path
    if output_path is not None:
        config.output_path_html = output_path[:output_path.rfind('.')] + '.html'
    config.objective = objective
    config.fraction = fraction_of_optimum
    config.processes = 1

    LOGGER.info("FRACTION: " + str(config.fraction))

    facade = Facade()
    facade.generate_critical_cp_report(config)

    _, filename1 = ntpath.split(config.output_path_html)
    _, filename2 = ntpath.split(config.output_path_spreadsheet)
    return (filename1, filename2)

def compute_growth_dependent_reactions(model_path, output_path, objective=None, model_uuid=None):

    def verbose_f(text, args1=None, args2=None):
        '''
        args1 = ws room name
        args2 = None
        '''
        LOGGER.info(text)
        send_message_client(args1, text)

    config = GrowthDependentCPConfig()
    config.model_path = model_path
    config.print_f = verbose_f
    config.args1 = model_uuid
    config.args2 = None
    config.output_path_spreadsheet = output_path
    if output_path is not None:
        config.output_path_html = output_path[:output_path.rfind('.')] + '.html'
    config.objective = objective
    config.processes = 1

    facade = Facade()
    facade.generate_growth_dependent_report(config)

    _, filename1 = ntpath.split(config.output_path_html)
    _, filename2 = ntpath.split(config.output_path_spreadsheet)
    return (filename1, filename2)

