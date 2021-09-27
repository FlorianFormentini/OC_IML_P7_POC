# import json
from flask_restx import abort
from flask import current_app  # jsonify
# from werkzeug.exceptions import HTTPException

from ...core.chatbot import Chatbot
from ...database.mongodb.DAL.base_dao import _chatbot_dao
# from ..utils import file_upload


class ChatbotServices:
    def __init__(self, dao):
        self.dao = dao

    # use doa to save message with intent + proba + resp

    def ask(self, input):
        try:
            chatbot = Chatbot(
                current_app.config['CHATBOT_PATH']['vectorizer_responses'],
                current_app.config['CHATBOT_PATH']['model'],
                current_app.config['PRED_THRESHOLD']
            )
            predicted_intents = chatbot.predict_intent(input)
            print('prediction :', predicted_intents)
            resp = chatbot.get_response(predicted_intents[0]['intent'])
            return {'message': resp}
        except Exception as e:
            abort(500, e)

    def get_known_intents(self):
        try:
            chatbot = Chatbot(
                current_app.config['CHATBOT_PATH']['vectorizer_responses'],
                current_app.config['CHATBOT_PATH']['model'],
                current_app.config['PRED_THRESHOLD']
            )
            chatbot.label_binarizer.classes_
            intents = chatbot.label_binarizer.classes_
            if not intents:
                abort(404, 'No data found.')
            return intents
        except Exception as e:
            abort(500, e)


# singleton object to use in the controllers
_chatbot_services = ChatbotServices(_chatbot_dao)
