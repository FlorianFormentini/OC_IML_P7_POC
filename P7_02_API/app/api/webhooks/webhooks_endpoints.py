from flask import request
from flask_restx import Resource

from .webhooks_dto import WebhooksDTO
from .webhooks_services import _webhooks_services

from ..utils import apikey_required

# ns declaration is in DTO to avoid circular imports and because it have to be loaded before the routes
ns = WebhooksDTO.ns


@ns.route('/TelegramWebhook')
# @ns.doc(params={'token': 'Telegram bot token'})
# @ns.response(403, 'Invalid Telegram bot token')
class TelegramWebhook(Resource):

    @ns.doc(security=None)
    @ns.response(200, "Success")
    def get(self):
        """Set / Unset the Telegram Webhook"""
        # param in url to set/unset webhook (+parsers)
        return _webhooks_services.telegram_webhook_set()

    @ns.doc(security=None)
    @ns.response(201, 'Telegram event successfully processed')
    def post(self):
        """Handle new Telegram events"""
        data = request.get_json()
        return _webhooks_services.handle_telegram_event(data)


@ns.route('/FacebookWebhook')
class FacebookWebhook(Resource):
    @ns.doc(params={
        'hub.mode': 'This value will always be "subscribe"',
        'hub.verify_token': 'Facebook App VERIFY_TOKEN',
        'hub.challenge': 'The expected response created by Facebook'
        }, security=None)
    @ns.expect(WebhooksDTO.fb_verif_webhook)
    @ns.response(401, 'Verify tokens do not match')
    @ns.response(400, 'A param is missing in the request')
    def get(self):
        """Handle Facebook's webhook verifications"""
        args = WebhooksDTO.fb_verif_webhook.parse_args(request)
        return _webhooks_services.fb_webhook_verif(args['hub.verify_token'], args['hub.challenge'])

    @ns.doc(security=None)
    @ns.expect(WebhooksDTO.fb_event_in)
    @ns.response(201, 'Facebook event successfully processed')
    @ns.response(404, 'Not an event from a Page subscription')
    def post(self):
        """Handle new Facebook events"""
        return _webhooks_services.handle_fbevent(data=request.get_json())


@ns.route('/events')
class EventList(Resource):
    @apikey_required
    @ns.marshal_list_with(WebhooksDTO.event_out)
    @ns.expect(WebhooksDTO.filterlist_args)
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
        filters = WebhooksDTO.filterlist_args.parse_args(request)
        return _webhooks_services.get_event_list(filters)

    @apikey_required
    @ns.doc(security='apikey')
    @ns.expect(WebhooksDTO.fb_event_in)
    @ns.response(201, 'Event successfully created.')
    @ns.response(400, 'Data validation error')
    @ns.response(401, "Wrong API key")
    def post(self):
        """Creates a new Event from the API"""
        return _webhooks_services.create_event(data=request.json)

    @apikey_required
    @ns.doc(security='apikey')
    @ns.response(200, 'All events successfully deleted.')
    @ns.response(401, "Wrong API key")
    def delete(self):
        """Delete all events"""
        return _webhooks_services.delete_events(mode='all')


@ns.route('/event/<id>')
@ns.doc(params={'id': 'An event ID'})
@ns.response(404, 'Event not found.')
class EventItem(Resource):
    @apikey_required
    @ns.doc(security='apikey')
    @ns.response(401, "Wrong API key")
    @ns.marshal_with(WebhooksDTO.event_out)
    def get(self, id):
        """Get an event given its identifier"""
        return _webhooks_services.get_event(id)

    @apikey_required
    @ns.doc(security='apikey')
    @ns.response(200, 'Event successfully deleted.')
    @ns.response(401, "Wrong API key")
    def delete(self, id):
        """Delete an event given its identifier"""
        return _webhooks_services.delete_events(mode='one', filters=id)
