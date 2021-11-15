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

# from src.restapi.repository.ModelRepositoryMongo import ModelRepository
from src.restapi.repository.ModelRepositoryMysqlAlchemy import ModelRepository


class ModelService:
    model_repository = ModelRepository()

    def insert(self, uuid, url):
        self.model_repository.insert(uuid, url)

    def query_by_uuid(self, uuid):
        result = self.model_repository.query_by_uuid(uuid)
        if result is None:
            raise RuntimeError("Error fetching submit")
        else:
            return result

    def query(self):
        return self.model_repository.query()
