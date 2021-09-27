import requests
from flask import current_app
from flask_restx import abort

from .chatbot import _chatbot


class TelegramBot:
    """Telegram bot business methods"""

    # ajouter méthodes set/unset webhook ici et une seule méthode qui fait les 2 dans services

    @staticmethod
    def map_telegram_event(data):
        """Mapping of a Telegram event to the db model struct
        args:
            data (dict) - Telegram event raw data
        returns:
            mapped_event (dict) - Mapped Telegram event
        """
        mapped_event = {

        }
        return mapped_event

    @staticmethod
    def send_message(message, chatid):
        """Computes a response and sends it to the Telegram API
        args:
            message (str) - Telegram user input
            message (chatid) - Telegram chat id
        """
        # chatbot response
        predicted_intents = _chatbot.predict_intent(message)
        print('prediction :', predicted_intents)
        msg = _chatbot.get_response(predicted_intents[0]['intent'])
        payload = {
            "text": msg,
            "chat_id": chatid
        }
        # send get request to the Telegram API's /sendMessage endpoint
        r = requests.get(f"{current_app.config['TELEGRAM_BOT_URL']}/sendMessage", params=payload)
        if r.status_code != 200:
            abort(r.status_code, r.text)
        else:
            print('Message successfully transmitted to the Telegram API')
