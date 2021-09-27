from flask_restx import Namespace, fields, reqparse, inputs


class WebhooksDTO:
    # ### Namespace declaration ###
    # #############################
    ns = Namespace('Webhooks', description='Social Networks webhooks suppport')

    # ### Input data model ###
    # ########################
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

    # Output data model
    fb_attachment_out = ns.model('attachment_out', {
        'type': fields.String(required=True, description='Attachement type'),
        'url': fields.String(required=True, description='Link'),
    })
    event_out = ns.model('event_out', {
        'id': fields.String(required=True, description='Event identifier'),  # for testing purpose
        'psid': fields.String(required=True, description='Page sender id'),
        'recipient_id': fields.String(required=True, description='Id of the recipient page'),
        'timestamp': fields.Integer(required=True, description='Reception time'),
        'message': fields.String(description='Received message'),
        'predicted_intent': fields.String(description='Intent predicted by the chatbot'),
        'postback': fields.String(description='Received postback'),
        'attachments': fields.List(fields.Nested(fb_attachment_out), description='List of attachments')
    })

    # ### Requests params ###
    # #######################
    # Event creation
    filterlist_args = reqparse.RequestParser()
    filterlist_args.add_argument('psid', type=str, required=False)
    filterlist_args.add_argument('recipient_id', type=str, required=False)
    filterlist_args.add_argument('messages', type=inputs.boolean, default=False, required=False)
    filterlist_args.add_argument('postbacks', type=inputs.boolean, default=False, required=False)
    # filterlist_args.add_argument('csv', type=bool, required=False)

    # Facebook webhook validation
    fb_verif_webhook = reqparse.RequestParser()
    fb_verif_webhook.add_argument('hub.mode', type=str, required=True)
    fb_verif_webhook.add_argument('hub.verify_token', type=str, required=True)
    fb_verif_webhook.add_argument('hub.challenge', type=int, required=True)
