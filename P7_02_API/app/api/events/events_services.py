from flask_restx import abort
from werkzeug.exceptions import NotFound

from ...database.mongodb.DAL.base_dao import _events_dao


class EventsServices:
    def __init__(self, dao):
        self.dao = dao

    def get_event(self, id):
        """Gets an event by id
        args:
            id (str) - Event ID
        returns:
            (Event)
        """
        try:
            event = self.dao.get_one(id=id)
            if not event:
                abort(404, 'No Event found.')
            return event
        except Exception as e:
            return abort(400, e)

    def get_event_list(self, filters):
        """Gets a list of events. Return all avents if no filter given
        args:
            filters (dict) - To filter the returned event list
        returns:
            (list(Event))
        """
        try:
            if not any(filters.values()):
                # all events if no filter
                events_list = self.dao.get_all()
            else:
                # handle the 'messages' and 'postbacks' filters
                filters['message__exists'] = filters['messages']
                del filters['messages']
                filters['postback__exists'] = filters['postbacks']
                del filters['postbacks']

                events_list = self.dao.get_list(filters)
            if not events_list:
                abort(404, 'No Event found.')
            print([event.to_json() for event in events_list])

            return [event for event in events_list]
        except NotFound:
            if any(filters.values()):
                msg = 'No Event found with these filters'
            else:
                msg = 'The collection is empty'
            abort(404, message=msg)
        except Exception as e:
            abort(400, message=e)

    def create_event(self, data, source):
        """Inserts a single event in the db from the API. The event is mapped according to the past sourc
        ars:
            data (dict) - Event data
            source (str) - Event source
        """
        try:
            for entry in data['entry']:
                event_data = entry['messaging'][0]
                if source == 'facebook':
                    mapped_event = self.__map_fb_event(event_data)
                print('fb services', mapped_event)
                self.dao.insert(data=mapped_event)
            return {'message': 'Event created'}, 201
        except Exception as e:
            return abort(400, e)

    def delete_events(self, mode, filters=None):
        """Deletes events from the db.
        args:
            mode (str) {'one', 'multi', 'all'} - Removing mode
            filters (dict) default=None - To filter the event list to delete
        """
        try:
            if filters and mode == 'one':
                self.dao.delete_one(id=filters)
                msg = 'Event deleted'
            elif filters and mode == 'multi':
                # not implemented in the routes yet
                self.dao.delete_bulk(filters)
                msg = 'Event list deleted'
            else:
                self.dao.delete_all()
                msg = 'All events and their attachements deleted'
            return {'message': msg}
        except AttributeError:
            return abort(404, f"No Event found with this id ('{filters}')")


# singleton object to use in the controllers
_events_services = EventsServices(_events_dao)
