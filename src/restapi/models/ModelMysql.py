from src.restapi.database import db

class Models(db.Model):
    __tablename__ = 'MODELS'
    uuid = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    url = db.Column(db.Text, unique=True, nullable=False)
