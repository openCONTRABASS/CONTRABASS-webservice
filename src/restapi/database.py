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

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import QueuePool

# https://stackoverflow.com/questions/58659316/pymysql-err-operationalerror-2013-lost-connection-to-mysql-server-during-que
# https://docs.sqlalchemy.org/en/13/core/pooling.html#setting-pool-recycle
db = SQLAlchemy(engine_options={"pool_size": 10, "poolclass":QueuePool, "pool_pre_ping":True, "pool_recycle": 3600})
