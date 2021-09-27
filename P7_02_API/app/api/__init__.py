from flask import Blueprint, current_app
from flask_restx import Api, abort

from .utils import authorizations
from .webhooks.webhooks_endpoints import ns as ns_webhooks
from .chatbot.chatbot_endpoints import ns as chatbot_ns


# API Blueprint declaration
api_blueprint = Blueprint('api', __name__)
api = Api(
    api_blueprint,
    authorizations=authorizations,
    title='OC-IML-P7 : Chatbot API',
    version='1.0',
    description='Endpoints to connect the chatbot to a channel (Facebook or Telegram) and speak with it'
)

# subscription to all namespaces
api.add_namespace(chatbot_ns, path='/chatbot')
api.add_namespace(ns_webhooks, path='/webhooks')

@api.errorhandler
def default_error_handler(e):
    if not current_app.config['DEBUG']:
        abort(500, f'An unhandled exception occurred : {e}')
