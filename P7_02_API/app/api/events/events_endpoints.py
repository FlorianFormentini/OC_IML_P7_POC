from flask import request
from flask_restx import Resource

from .events_services import _events_services
from .events_dto import EventsDTO
from ..utils import apikey_required

ns = EventsDTO.ns


@ns.route('/events')
class EventList(Resource):
    @apikey_required
    @ns.marshal_list_with(EventsDTO.event_out)
    @ns.expect(EventsDTO.filterlist_args)
    @ns.doc(params={
        'psid': 'To filter by PageSenderID',
        'recipient_id': 'To filter by Recipient ID',
        'messages': 'Get messages only',
        'postbacks': 'Get postbacks only',
        'begin': 'Get events created after this date'}, security='apikey')
    @ns.response(200, 'Success')
    @ns.response(401, "Wrong API key")
    def get(self):
        """
        List all registered events
        The list can be filtered by passing with these parameters :
        """
        filters = EventsDTO.filterlist_args.parse_args(request)
        return _events_services.get_event_list(filters)

    @apikey_required
    @ns.doc(security='apikey')
    @ns.response(200, 'All events successfully deleted.')
    @ns.response(401, "Wrong API key")
    def delete(self):
        """Delete all events"""
        return _events_services.delete_events(mode='all')


@ns.route('/event/<id>')
@ns.doc(params={'id': 'An event ID'})
@ns.response(404, 'Event not found.')
class EventItem(Resource):
    @apikey_required
    @ns.doc(security='apikey')
    @ns.response(401, "Wrong API key")
    @ns.marshal_with(EventsDTO.event_out)
    def get(self, id):
        """Get an event given its identifier"""
        return _events_services.get_event(id)

    @apikey_required
    @ns.doc(security='apikey')
    @ns.response(200, 'Event successfully deleted.')
    @ns.response(401, "Wrong API key")
    def delete(self, id):
        """Delete an event given its identifier"""
        return _events_services.delete_events(mode='one', filters=id)
