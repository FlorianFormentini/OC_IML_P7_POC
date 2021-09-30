from flask import request
from flask_restx import Resource

from .webhooks_dto import WebhooksDTO
from .webhooks_services import _webhooks_services


# ns declaration is in DTO to avoid circular imports and because it have to be loaded before the routes
ns = WebhooksDTO.ns


@ns.route('/TelegramWebhook')
# @ns.doc(params={'token': 'Telegram bot token'})
# @ns.response(403, 'Invalid Telegram bot token')
class TelegramWebhook(Resource):

    @ns.doc(security=None)
    @ns.expect(WebhooksDTO.telegram_webhook_args)
    @ns.response(200, "Success")
    def get(self):
        """Set / Unset the Telegram Webhook"""
        args = WebhooksDTO.telegram_webhook_args.parse_args(request)
        if args['set']:
            return _webhooks_services.set_telegram_webhook()
        else:
            return _webhooks_services.unset_telegram_webhook()

    @ns.doc(security=None)
    @ns.response(201, 'Telegram event successfully processed')
    def post(self):
        """Handle new Telegram events"""
        return _webhooks_services.handle_telegram_event(data=request.get_json())


@ns.route('/FacebookWebhook')
class FacebookWebhook(Resource):
    @ns.doc(params={
        'hub.mode': 'This value will always be "subscribe"',
        'hub.verify_token': 'Facebook App VERIFY_TOKEN',
        'hub.challenge': 'The expected response created by Facebook'
        }, security=None)
    @ns.expect(WebhooksDTO.fb_webhook_args)
    @ns.response(401, 'Verify tokens do not match')
    @ns.response(400, 'A param is missing in the request')
    def get(self):
        """Handle Facebook's webhook verifications"""
        args = WebhooksDTO.fb_webhook_args.parse_args(request)
        return _webhooks_services.set_fb_webhook(args['hub.verify_token'], args['hub.challenge'])

    @ns.doc(security=None)
    @ns.expect(WebhooksDTO.fb_event_in)
    @ns.response(201, 'Facebook event successfully processed')
    @ns.response(404, 'Not an event from a Page subscription')
    def post(self):
        """Handle new Facebook events"""
        return _webhooks_services.handle_fb_event(data=request.get_json())
