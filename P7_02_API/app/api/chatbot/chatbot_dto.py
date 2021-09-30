from flask_restx import Namespace, fields, reqparse
from werkzeug.datastructures import FileStorage


class ChatbotDTO:
    # Namespace declaration
    ns = Namespace('Chatbot', description='Chatbot management')

# ### Data validation ###

    chatbot_intents_out = ns.model('message', {
        'tag': fields.String(description='Intents'),
        'patterns': fields.List(fields.String(), description='Intents patterns'),
        'responses': fields.List(fields.String(), description='Intents responses')
    })

    event_in = ns.model('event_input', {
        'id': fields.String(required=False, description='Event identifier'),  # for testing purpose
        'message': fields.String(description='Received message'),
    })

# ### Requests params ###

    # Chatbot data upload
    data_upload_args = reqparse.RequestParser()
    data_upload_args.add_argument(
        'json_datafile',
        type=FileStorage,
        location='files',
        required=False
    )
