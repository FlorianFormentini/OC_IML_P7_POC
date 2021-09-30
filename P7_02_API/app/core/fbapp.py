import requests
from flask import current_app

from .chatbot import Chatbot


class FbApp:
    """Facebook App business methods"""

    @staticmethod
    def map_fb_event(data):
        """Mapping of a Facebook event to the db model struct
        args:
            data (dict) - Facebook event raw data
        returns:
            mapped_event (dict) - Mapped fb event
        """
        mapped_event = {
            'source': 'Facebook',
            'user_id': data['sender']['id'],
            'timestamp': data['timestamp'],
            # get() used on optionnal fields to not raise an error
            'message': data.get('message', {}).get('text'),
        }
        return mapped_event

    @staticmethod
    def send_fb_message(cls, sender_psid, message):
        """Sends a response with the Facebook Send API (POST request)
        args:
            sender_psid (str) - Facebook user PSID
            message (str) - Response to transmit
        """
        reqBody = {
            "recipient": {
                "id": sender_psid
            },
            "message": message
        }
        # POST request to the Facebook Send API
        r = requests.post(
            current_app.config['FB_SEND_API_URL'],
            params={'access_token': current_app.config['PAGE_ACCESS_TOKEN']},
            headers={'Content-Type': 'application/json'},
            json=reqBody
        )
        return r

    @classmethod
    def compute_msg_response(cls, message):
        """Computes a response for a Facebook message
        args:
            senderPsid (str) - Facebook user PSID
            message (str) - Facebook user input
        returns:
            (str) - Response message
        """
        # here condition to use integrated bot or Rasa bot
        chatbot = Chatbot(
            current_app.config['CHATBOT_PATH']['vectorizer_responses'],
            current_app.config['CHATBOT_PATH']['model'],
            current_app.config['PRED_THRESHOLD']
        )
        print("message = ", message)
        predicted_intents = chatbot.predict_intent(message)
        print('prediction :', predicted_intents)
        msg = chatbot.get_response(predicted_intents[0]['intent'])
        response = {
            "intent": predicted_intents,
            "text": msg
        }
        return response

    @classmethod
    def compute_attachement_response(cls, senderPsid):
        """Copute a reponse for an attachements without any text message
        args:
            senderPsid (str) - Facebook user PSID
        """
        img_url = 'https://media.giphy.com/media/7rn4LNw0nwewrupGor/giphy.gif'
        response = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [{
                        'title': "Oups ! Je n'ai pas compris...",
                        'subtitle': "Essayez de me poser une question",
                        'image_url': img_url,
                    }]
                }
            }
        }
        return response

    # @classmethod
    # def postback_reply(cls, senderPsid, postback):
    #     """Computes a response for a postback after a facebook form
    #     args:
    #         senderPsid (str) - Facebook user PSID
    #         postback (str) - Facebook user postback
    #     """
    #     payload = postback['payload']
    #     if payload == 'yes':
    #         resp = {'text': 'Ok ! :)'}
    #     else:
    #         resp = {'text': 'Dommage...'}
    #     cls.callSendAPI(senderPsid, resp)
