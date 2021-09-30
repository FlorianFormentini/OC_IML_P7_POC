from flask import Blueprint, current_app
from flask_restx import Api, abort

from .utils import authorizations
from .webhooks.webhooks_endpoints import ns as ns_webhooks
from .chatbot.chatbot_endpoints import ns as ns_chatbot
from .events.events_endpoints import ns as ns_events


# API Blueprint declaration
api_blueprint = Blueprint('api', __name__)
api = Api(
    api_blueprint,
    authorizations=authorizations,
    title='OC IML P7 - Chatbot API',
    version='1.0',
    description='OpenClassrooms - Ingénieur MAchine Learning - Project 07\nAPI to speak with the chatbot\nFlorian Formentini (10/2021)'
)

# subscription to all namespaces
api.add_namespace(ns_chatbot, path='/chatbot')
api.add_namespace(ns_webhooks, path='/webhooks')
api.add_namespace(ns_events, path='/events')


@api.errorhandler
def default_error_handler(e):
    if not current_app.config['DEBUG']:
        abort(500, f'An unhandled exception occurred : {e}')
