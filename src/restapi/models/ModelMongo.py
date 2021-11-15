from src.restapi.database import db

db.connect('models')

class Model(db.Document):

    uuid = db.StringField(unique=True, required=True)
    url  = db.StringField(required=True)

