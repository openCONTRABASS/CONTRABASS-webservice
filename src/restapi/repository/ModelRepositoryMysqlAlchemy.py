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

from src.restapi.models.ModelMysql import Models
from src.restapi.exceptions import *
from src.restapi.database import db

LOGGER = logging.getLogger(__name__)


class ModelRepository:

    def insert(self, uuid, url):
        LOGGER.info(f"Saving Models(uuid={uuid}, url={url})")
        models = Models(uuid=uuid, url=url)
        db.session.add(models)
        db.session.commit()

    def query_by_uuid(self, uuid):
        LOGGER.info(f"Quering Model(uuid={uuid})")
        model = Models.query.filter_by(uuid=str(uuid)).first()
        if model is None:
            raise NotFoundException()
        else:
            return model
