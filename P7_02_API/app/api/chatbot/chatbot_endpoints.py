from flask_restx import Resource

from .chatbot_services import _chatbot_services
from ..utils import apikey_required
from .chatbot_dto import ChatbotDTO


ns = ChatbotDTO.ns


@ns.route('/data')
class ChatbotData(Resource):
    # @apikey_required
    # @ns.doc(security='apikey')
    # @ns.expect(ChatbotDTO.data_upload_args)
    # @ns.response(200, 'File successfully processed.')
    # @ns.response(400, 'File error')
    # @ns.response(401, "Wrong API key")
    # def post(self):
    #     """Endpoint to upload the chatbot dataset"""
    #     args = ChatbotDTO.data_upload_args.parse_args()
    #     return _chatbot_services.upload_dataset(args['json_datafile'])

    @apikey_required
    @ns.doc(security='apikey')
    @ns.marshal_list_with(ChatbotDTO.chatbot_intents_out)
    @ns.response(401, "Wrong API key")
    def get(self):
        """List all chatbot known intents"""
        return _chatbot_services.get_chatbot_intents()


@ns.route('/rest/<question>')
class ChatbotTests(Resource):

    @apikey_required
    @ns.doc(security='apikey')
    # @ns.expect(ChatbotDTO.question)
    @ns.response(200, 'Success')
    @ns.response(500, 'A problem occurred with the chatbot.')
    @ns.response(401, "Wrong API key")
    def post(self, question):
        """Endpoint to ask the chatbot a question."""
        print(question)
        return _chatbot_services.ask_chatbot(question)
