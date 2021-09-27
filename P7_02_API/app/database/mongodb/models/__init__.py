from .. import db


class FbEvent(db.Document):
    name = db.StringField()
