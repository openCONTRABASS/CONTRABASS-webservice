import logging

from src.restapi.models.ModelMongo import Model
from src.restapi.exceptions import *

from pymongo.errors import DuplicateKeyError
from mongoengine import NotUniqueError

LOGGER = logging.getLogger(__name__)


class ModelRepository:

    def insert(self, uuid, url):
        try:
            LOGGER.info(f"Saving Model(uuid={uuid}, url={url})")
            Model(uuid=uuid, url=url).save()
        except (NotUniqueError, DuplicateKeyError) as err:
            raise DuplicateException()


    def query_by_uuid(self, uuid):
        LOGGER.info(f"Quering Model(uuid={uuid})")
        value = Model.objects(uuid=str(uuid)).first()
        if value is None:
            raise NotFoundException()
        else:
            return value

    def query(self):
        return Model.objects.all()