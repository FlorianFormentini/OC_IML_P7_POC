from ..models.chatbot_intents_model import ChatbotIntent
from ..models.event_model import Event


class BaseDAO:
    """Base Data Access Objects Class - Contains base methods to manipulate data"""

    def __init__(self, model):
        self.model = model

    def get_one(self, **kwargs):
        return self.model.objects(**kwargs).first()

    def get_list(self, filters):
        obj_list = self.model.objects(**filters)
        return obj_list

    def get_all(self):
        return self.model.objects()

    def insert(self, data=None, **kwargs):
        obj_data = data or kwargs
        obj = self.model(**obj_data)
        obj.save()

    def insert_bulk(self, data):
        event_list = [self.model(**event) for event in data]
        self.model.objects.insert(event_list)

    def delete_one(self, filters=None, **kwargs):
        search_filters = filters or kwargs
        obj = self.model.objects(**search_filters).first()
        obj.delete()

    def delete_bulk(self, filters=None, **kwargs):
        search_filters = filters or kwargs
        self.model.objects(**search_filters).delete()

    def delete_all(self):
        self.model.objects().delete()


# singleton objects to use eslsewhere in the app
_events_dao = BaseDAO(Event)
_chatbot_dao = BaseDAO(ChatbotIntent)
