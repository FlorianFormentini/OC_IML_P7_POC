from flask_restx import Namespace, fields, reqparse, inputs
from werkzeug.datastructures import FileStorage


class ChatbotDTO:
    # Namespace declaration
    ns = Namespace('Chatbot', description='Chatbot management')

    # Output data model
    chatbot_intents_out = ns.model('message', {
        'tag': fields.String(description='Intents'),
        'patterns': fields.List(fields.String(), description='Intents patterns'),
        'responses': fields.List(fields.String(), description='Intents responses')
    })

    # Requests args
    data_upload_args = reqparse.RequestParser()
    data_upload_args.add_argument(
        'json_datafile',
        type=FileStorage,
        location='files',
        required=False
    )
    data_upload_args.add_argument('new_training', type=inputs.boolean, default=False, required=False)
