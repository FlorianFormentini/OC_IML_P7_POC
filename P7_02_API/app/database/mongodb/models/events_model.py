from .. import db


class Event(db.Document):
    source = db.StringField(required=True)
    user_id = db.StringField()
    user_name = db.StringField()
    timestamp = db.IntField(required=True)
    message = db.StringField(required=True)
    predicted_intent = db.StringField()

    meta = {
        'collection': 'events',
    }

    def __repr__(self):
        return f'<FB Event {self.id}>'
