from .. import db


class ChatbotIntent(db.Document):
    tag = db.StringField(required=True)
    patterns = db.ListField(db.StringField(), required=True)
    responses = db.ListField(db.StringField(), required=True)
    context = db.ListField(db.StringField(), default=[""])

    meta = {
        'collection': 'chatbot_intents'
    }

    def __repr__(self):
        return f'<Chatbot Intent {self.tag}>'
