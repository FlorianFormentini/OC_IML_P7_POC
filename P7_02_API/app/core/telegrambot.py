import requests
from flask import current_app

from .chatbot import Chatbot


class TelegramBot:
    """Telegram bot business methods"""
    @staticmethod
    def map_telegram_event(data):
        """Mapping of a Telegram event to the db model struct
        args:
            data (dict) - Telegram event raw data
        returns:
            mapped_event (dict) - Mapped Telegram event
        """
        mapped_event = {
            'source': 'Telegram',
            'user_id': data['sender']['id'],
            'timestamp': data['timestamp'],
            # get() used on optionnal fields to not raise an error
            'message': data.get('message', {}).get('text'),
        }
        return mapped_event

    @staticmethod
    def send_telegram_message(message, chatid):
        """Computes a response and sends it to the Telegram API
        args:
            message (str) - Telegram user input
            message (chatid) - Telegram chat id
        returns:
            requests.Response - Telegram API response
        """
        chatbot = Chatbot(
            current_app.config['CHATBOT_PATH']['vectorizer_responses'],
            current_app.config['CHATBOT_PATH']['model'],
            current_app.config['PRED_THRESHOLD']
        )
        # chatbot response
        predicted_intents = chatbot.predict_intent(message)
        print('prediction :', predicted_intents)
        msg = chatbot.get_response(predicted_intents[0]['intent'])
        payload = {
            "text": msg,
            "chat_id": chatid
        }
        # send get request to the Telegram API's /sendMessage endpoint
        r = requests.get(f"{current_app.config['TELEGRAM_BOT_URL']}/sendMessage", params=payload)
        return r
