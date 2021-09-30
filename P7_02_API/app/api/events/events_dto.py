from flask_restx import Namespace, fields, reqparse, inputs


class EventsDTO:
    # Namespace declaration
    ns = Namespace('Events', description='Events management')

# ### Data validation models ###

    event_out = ns.model(name='event_output', model={
        'id': fields.String(required=True, description='Event identifier'),  # for testing purpose
        'source': fields.String(required=True, description='Event source'),
        'user_id':  fields.String(required=True, description='User id'),
        'user_name': fields.String(required=True, description='User name'),
        'timestamp': fields.Integer(required=True, description='Message date'),
        'message': fields.String(required=False, description='Message text'),
        'predicted_intent': fields.String(required=False, description='Predicted intent'),
        'chatbot_response': fields.String(required=False, description='Event identifier'),
    })

# ### Request params ###

    # Event creation
    filterlist_args = reqparse.RequestParser()
    filterlist_args.add_argument('psid', type=str, required=False)
    filterlist_args.add_argument('recipient_id', type=str, required=False)
    filterlist_args.add_argument('messages', type=inputs.boolean, default=False, required=False)
    filterlist_args.add_argument('postbacks', type=inputs.boolean, default=False, required=False)
