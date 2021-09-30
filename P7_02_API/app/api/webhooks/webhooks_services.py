from flask import current_app
from flask_restx import abort

import requests

from ...core.fbapp import FbApp
from ...core.telegrambot import TelegramBot
from ...database.mongodb.DAL.base_dao import BaseDAO, _events_dao


class WebhookServices:
    def __init__(self, dao: BaseDAO):
        self.dao = dao

# ### Facebook Webhook ###

    def set_fb_webhook(self, verify_token, challenge):
        """Handles facebook webhook's verifications
        args:
            verify_token (str) - Facebook verify token
            challenge (int) - Value to return to validate the webhook
        returns
            challenge (int)
        """
        if verify_token == current_app.config['FB_VERIFY_TOKEN']:
            return challenge, 200
        else:
            abort(403, "Invalid Facebook verify token")

    def handle_fb_event(self, data):
        """Facebook events processing
        args:
            data (dict) - Raw Facebook event data
        """
        try:
            if data['object'] == 'page':
                for entry in data['entry']:
                    # get event data
                    webhookEvent = entry['messaging'][0]
                    # format event data
                    mapped_event = FbApp.map_fb_event(webhookEvent)
                    # event processing
                    if mapped_event.get('message'):
                        # reply to a text message
                        response = FbApp.compute_msg_response(mapped_event['user_id'], mapped_event['message'])
                        mapped_event['predicted_intent'] = response['intent']
                        mapped_event['chatbot_response'] = response['text']
                        # saving event in db
                        self.dao.insert(data=mapped_event)
                    else:
                        # reply to attachements without text message
                        if mapped_event.get('attachments'):
                            FbApp.compute_attachement_response(mapped_event['user_id'], mapped_event['attachments'])
                        # FbApp.handle_postback(senderPsid, mapped_event['postback'])

                    # reply to user
                    fb_api_res = FbApp.call_send_api(mapped_event['user_id'], response)
                    if fb_api_res.status_code != 200:
                        abort(fb_api_res.status_code, fb_api_res.text)

                return {'message': 'Facebook event successfully processed'}, 201
            else:
                abort(404, 'Not an event from a Page subscription')
        except Exception as e:
            abort(500, f'Error : {e}')

# ### Telegram Webhook ###

    def set_telegram_webhook(self):
        """Handles Telegram webhook's activation"""
        host_url = current_app.config['HOST_URL']
        telegram_url = current_app.config['TELEGRAM_BOT_URL']
        # GET request to Telegram API's /setWebhook to activate bot's webhook on TelegramWebhook endpoint
        r = requests.get(f"{telegram_url}/setWebhook?url={host_url}/webhooks/TelegramWebhook")
        if r:
            return {'message': 'Telegram webhook successfully set'}, 200
        else:
            abort(r.status_code, f"Telegram webhook setup failed : {r.text}")

    def unset_telegram_webhook(self):
        """Handles Telegram webhook's deactivation"""
        host_url = current_app.config['HOST_URL']
        telegram_url = current_app.config['TELEGRAM_BOT_URL']
        # GET request to Telegram API's /deleteWebhook to delete bot's webhook on /TelegramWebhook endpoint
        r = requests.get(f"{telegram_url}/deleteWebhook?url={host_url}/webhooks/TelegramWebhook")
        if r:
            return {'message': 'Telegram webhook successfully deleted'}, 200
        else:
            abort(r.status_code, f"Telegram webhook setup failed : {r.text}")

    def handle_telegram_event(self, data):
        """Telegram events processing
        args:
            data (dict) - Raw Telegram event
        """
        try:
            print('Telegram Event :', data)
            if 'text' in data['message']:
                msgtext = data["message"]["text"]
                # sendername = data["message"]["from"]["first_name"]
                chatid = data["message"]["chat"]["id"]
                # save entering event
                # transmit to telegram api
                api_res = TelegramBot.send_message(msgtext, chatid)
                if api_res.status_code != 200:
                    abort(api_res.status_code, api_res.text)
                else:
                    return {'message': 'Telegram event successfully processed'}, 201
        except Exception as e:
            abort(500, e)


# singleton object to use in the controllers
_webhooks_services = WebhookServices(_events_dao)
