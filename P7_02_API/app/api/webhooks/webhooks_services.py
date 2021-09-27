from flask import current_app
from flask_restx import abort
from werkzeug.exceptions import NotFound
import requests

from ...core.fbapp import FbApp
from ...core.telegrambot import TelegramBot
from ...database.mongodb.DAL.base_dao import BaseDAO, _event_dao


class WebhookServices:
    def __init__(self, dao: BaseDAO):
        self.dao = dao

# region Events CRUD
    def get_event(self, id):
        """Gets an event by id
        args:
            id (str) - Event ID
        returns:
            (Event)
        """
        try:
            event = self.dao.get_one(id=id)
            if not event:
                abort(404, 'No Event found.')
            return event
        except Exception as e:
            return abort(400, e)

    def get_event_list(self, filters):
        """Gets a list of events. Return all avents if no filter given
        args:
            filters (dict) - To filter the returned event list
        returns:
            (list(Event))
        """
        try:
            if not any(filters.values()):
                # all events if no filter
                events_list = self.dao.get_all()
            else:
                # handle the 'messages' and 'postbacks' filters
                filters['message__exists'] = filters['messages']
                del filters['messages']
                filters['postback__exists'] = filters['postbacks']
                del filters['postbacks']

                events_list = self.dao.get_list(filters)
            if not events_list:
                abort(404, 'No Event found.')
            print([event.to_json() for event in events_list])

            return [event for event in events_list]
        except NotFound:
            if any(filters.values()):
                msg = 'No Event found with these filters'
            else:
                msg = 'The collection is empty'
            abort(404, message=msg)
        except Exception as e:
            abort(400, message=e)

    def create_event(self, data, source):
        """Inserts a single event in the db from the API. The event is mapped according to the past sourc
        ars:
            data (dict) - Event data
            source (str) - Event source
        """
        try:
            for entry in data['entry']:
                event_data = entry['messaging'][0]
                if source == 'facebook':
                    mapped_event = self.__map_fb_event(event_data)
                print('fb services', mapped_event)
                self.dao.insert(data=mapped_event)
            return {'message': 'Event created'}, 201
        except Exception as e:
            return abort(400, e)

    def delete_events(self, mode, filters=None):
        """Deletes events from the db.
        args:
            mode (str) {'one', 'multi', 'all'} - Removing mode
            filters (dict) default=None - To filter the event list to delete
        """
        try:
            if filters and mode == 'one':
                self.dao.delete_one(id=filters)
                msg = 'Event deleted'
            elif filters and mode == 'multi':
                # not implemented in the routes yet
                self.dao.delete_bulk(filters)
                msg = 'Event list deleted'
            else:
                self.dao.delete_all()
                msg = 'All events and their attachements deleted'
            return {'message': msg}
        except AttributeError:
            return abort(404, f"No Event found with this id ('{filters}')")
# endregion

# region Facebook Webhook
    def handle_fbevent(self, data):
        """Facebook events processing
        args:
            data (dict) - Raw Facebook event data
        """
        try:
            if data['object'] == 'page':
                for entry in data['entry']:
                    # get webhook event
                    webhookEvent = entry['messaging'][0]
                    # format event data
                    mapped_event = FbApp.map_fb_event(webhookEvent)
                    print('mapped_event', mapped_event)
                    # get sender PSID
                    senderPsid = mapped_event['user_id']
                    # dispatch event
                    if mapped_event.get('attachments'):
                        FbApp.handle_attachments(senderPsid, mapped_event['attachments'])
                    if mapped_event['message']:
                        prediction = FbApp.handle_message(senderPsid, mapped_event['message'])
                        mapped_event['predicted_intent'] = prediction
                        # saving event in db
                        self.dao.insert(data=mapped_event)
                    else:
                        FbApp.handle_postback(senderPsid, mapped_event['postback'])
                return {'message': 'Event processed'}, 201
            else:
                abort(404, 'No an event from a Page subscription')
        except Exception as e:
            abort(500, f'Error : {e}')

    def fb_webhook_verif(self, verify_token, challenge):
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
            abort(403, "Invalid Facebook's verify token")
# endregion

# region Telegram
    def telegram_webhook_set(self):
        """Handles Telegram webhook's activation"""
        host_url = current_app.config['HOST_URL']
        telegram_url = current_app.config['TELEGRAM_BOT_URL']
        # GET request to Telegram API's /setWebhook to activate bot's webhook on TelegramWebhook endpoint
        r = requests.get(f"{telegram_url}/setWebhook?url={host_url}/webhooks/TelegramWebhook")
        if r:
            return {'message': 'Telegram webhook successfully set'}, 200
        else:
            abort(r.status_code, f"Telegram webhook setup failed : {r.text}")

    def telegram_webhook_delete(self):
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
                TelegramBot.send_message(msgtext, chatid)
        except Exception as e:
            abort(500, e)
# endregion


# singleton object to use in the controllers
_webhooks_services = WebhookServices(_event_dao)
