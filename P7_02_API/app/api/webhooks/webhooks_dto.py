from flask_restx import Namespace, fields, reqparse


class WebhooksDTO:
    # Namespace declaration
    ns = Namespace('Webhooks', description='Social Networks webhooks suppport')

# ### Data validation models ###

    # reproduce a simplified facebook data struct whith only fields that will be saved
    fb_att_payload = ns.model('attachment_payload', {
        'url': fields.String(required=True, description='attachment url'),
    })
    fb_msg_attachments = ns.model('attachments', {
        'type': fields.String(description='attachment type'),
        'payload': fields.Nested(fb_att_payload, required=True),
    })
    fb_message = ns.model('message', {
        'mid': fields.String(required=True, description='Message identifier'),
        'text': fields.String(description='Message content'),
        'attachments': fields.List(fields.Nested(fb_msg_attachments), description='List of attachments'),
    })
    fb_postback = ns.model('postback', {
        'payload': fields.String(required=True, description='Postback payload'),
    })
    fb_sender = ns.model('sender', {
        'id': fields.String(required=True, description='Page sender identifier'),
    })
    fb_recipient = ns.model('recipient', {
        'id': fields.String(required=True, description='Recipient page identifier'),
    })
    fb_messaging = ns.model('messaging', {
        'sender': fields.Nested(fb_sender, required=True, description='Sender data'),
        'recipient': fields.Nested(fb_recipient, required=True, description='Recipient page data'),
        'timestamp': fields.Integer(required=True, description='Reception time'),
        'message': fields.Nested(fb_message),
        'postback': fields.Nested(fb_postback),
    })
    fb_entry = ns.model('entry', {
        'messaging': fields.List(fields.Nested(fb_messaging), required=True, description='Event content - always contains a single object')
    })
    fb_event_in = ns.model('event_in', {
        'object': fields.String(required=True, description='Where the event come from'),
        'entry': fields.List(fields.Nested(fb_entry), required=True, description='Events batch'),
    })

# ### Requests params ###

    # Set Facebook webhook
    fb_webhook_args = reqparse.RequestParser()
    fb_webhook_args.add_argument('hub.mode', type=str, required=True)
    fb_webhook_args.add_argument('hub.verify_token', type=str, required=True)
    fb_webhook_args.add_argument('hub.challenge', type=int, required=True)

    # Set/unset Telegram webhook
    telegram_webhook_args = reqparse.RequestParser()
    telegram_webhook_args.add_argument('set', type=bool, required=True)
