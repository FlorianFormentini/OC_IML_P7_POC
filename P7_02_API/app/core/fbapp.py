import requests
from flask import current_app
from flask_restx import abort


from .chatbot import _chatbot


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

    @classmethod
    def callSendAPI(cls, senderPsid, response):
        """Sends a response to the Facebook API (POST request)
        args:
            senderPsid (str) - Facebook user PSID
            response (str) - Response to transmit
        """
        reqBody = {
            "recipient": {
                "id": senderPsid
            },
            "message": response
        }
        # POST request to the Facebook Send API
        r = requests.post(
            current_app.config['FB_SEND_API_URL'],
            params={'access_token': current_app.config['PAGE_ACCESS_TOKEN']},
            headers={'Content-Type': 'application/json'},
            json=reqBody
        )
        if r.status_code != 200:
            abort(r.status_code, r.text)
        else:
            print('Successfully transmitted to the Facebook Send API')

    @classmethod
    def handle_message(cls, senderPsid, message):
        """Computes a response for a Facebook message and return the predicted intent
        args:
            senderPsid (str) - Facebook user PSID
            message (str) - Facebook user input
        returns:
            (str) - Predicted intent for the user input
        """
        print("message = ", message)
        # Create the payload for a basic text messagewhich will be added to the body of your request to the Send API
        predicted_intents = _chatbot.predict_intent(message)
        print('prediction :', predicted_intents)
        msg = _chatbot.get_response(predicted_intents[0]['intent'])
        response = {
            "text": msg
        }
        # send response message
        cls.callSendAPI(senderPsid, response)
        return predicted_intents[0]['intent']

    @classmethod
    def handle_attachments(cls, senderPsid):
        """Computes a response for a Facebook attachement
        args:
            senderPsid (str) - Facebook user PSID
        """
        attachmentUrl = 'https://i.pinimg.com/originals/ec/6c/85/ec6c85439ea5235614deaaa2f12f4335.png'
        response = {
            'attachment': {
                'type': 'template',
                'payload': {
                    'template_type': 'generic',
                    'elements': [{
                        'title': "C'est une belle image !",
                        'subtitle': "Et que pensez-vous de celle-ci ? c'est moi :)",
                        'image_url': attachmentUrl,
                        'buttons': [
                            {
                                'type': 'postback',
                                'title': 'Trop mimi ! :D',
                                'payload': 'yes',
                            },
                            {
                                'type': 'postback',
                                'title': 'Euuh...',
                                'payload': 'no',
                            }
                        ],
                    }]
                }
            }
        }
        # send response message
        cls.callSendAPI(senderPsid, response)

    @classmethod
    def handle_postback(cls, senderPsid, postback):
        """Computes a response for a Facebook attachement
        args:
            senderPsid (str) - Facebook user PSID
            postback (str) - Facebook user postback
        """
        payload = postback['payload']
        if payload == 'yes':
            resp = {'text': 'Merci :)'}
        else:
            resp = {'text': 'Mince ! Montrez-moi en une qui vous plait'}
        cls.callSendAPI(senderPsid, resp)
