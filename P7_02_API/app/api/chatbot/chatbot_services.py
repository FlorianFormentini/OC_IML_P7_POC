# import json
from flask_restx import abort
from flask import current_app

from ...core.chatbot import Chatbot
# from ..utils import file_upload


class ChatbotServices:
    def __init__(self, dao=None):
        self.dao = dao

# ### Chatbot ####
    def ask_chatbot(self, input):
        """Send message to the chatbot
        Args:
            input (str): Input message

        Returns:
            dict: JSON Chatbot response (in 'message' key)
        """
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

    def get_chatbot_intents(self):
        """Returns the chatbot data
        Returns:
            list: []
        """
        try:
            chatbot = Chatbot(
                current_app.config['CHATBOT_PATH']['vectorizer_responses'],
                current_app.config['CHATBOT_PATH']['model'],
                current_app.config['PRED_THRESHOLD']
            )
            intents = chatbot.label_binarizer.classes_
            # responses = chatbot.responses
            if not intents:
                abort(404, 'No data found.')
            return intents
        except Exception as e:
            abort(500, e)


# singleton object to use in the controllers
_chatbot_services = ChatbotServices()
