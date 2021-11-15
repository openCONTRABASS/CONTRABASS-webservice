import logging

from src.restapi.models.ModelBean import Model
from src.restapi.exceptions import *


from restapi.database import connection

LOGGER = logging.getLogger(__name__)

INSERT_MODEL = 'INSERT INTO MODELS (UUID, URL) VALUES (% s, % s)'
QUERY_MODEL = 'SELECT * FROM MODELS WHERE uuid = % s'

class ModelRepository:

    def log_insert(self, query, args):
        query_log = query
        for par in list(args):
            query_log = query_log.replace('% s', par, 1)
        LOGGER.info(query_log)
        with connection.cursor() as cursor:
            print("Done cursor")
            cursor.execute(query,
                           args)
            print("Done execute")
            # Disabled to avoid: pymysql.err.Error: Already closed
            #connection.commit()

    def log_query_one(self, query, args):
        query_log = query
        for par in list(args):
            query_log = query_log.replace('% s', par, 1)
        LOGGER.info(query_log)
        with connection.cursor() as cursor:
            cursor.execute(query, args)
            result = cursor.fetchone()
            # Disabled to avoid: pymysql.err.Error: Already closed
            #cursor.close()
            return result
        return None

    def insert(self, uuid, url):
        self.log_insert(INSERT_MODEL, (uuid, url,))

    def query_by_uuid(self, uuid):
        uuid = str(uuid)
        model = Model()
        result = self.log_query_one(QUERY_MODEL, (uuid,))
        LOGGER.info(result)
        model.uuid = result["UUID"]
        model.url = result["URL"]
        return model

    #def query(self):
    #    return Model.objects.all()