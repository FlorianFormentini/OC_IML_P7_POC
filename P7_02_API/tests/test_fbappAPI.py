import unittest
import json
from flask import make_response
from timeit import default_timer as timer

from tests.base_test import BaseTestCase
from app.database import db
from app.database.models.event_model import Event
from app.api.fbapp.fbapp_services import _fbapp_services


class TestFbAppAPI(BaseTestCase):

    event_json = {
        "object": "string",
        "entry": [
            {
                "messaging": [
                    {
                        "sender": {
                            "id": "string"
                        },
                        "recipient": {
                            "id": "string"
                        },
                        "timestamp": 0,
                        "message": {
                            "mid": "string",
                            "text": "string",
                            "attachments": [
                                {
                                    "type": "string",
                                    "payload": {
                                        "url": "string"
                                    }
                                }
                            ]
                        },
                        "postback": {
                            "payload": "string"
                        }
                    }
                ]
            }
        ]
    }

    def __make_test_event(self, nb):
        evt_list = []
        for i in range(nb):
            test_event = Event(
                public_id='pid' + str(i),
                psid='psid' + str(i),
                recipient_id='recip' + str(i),
                mid='mid' + str(i),
                timestamp=i
            )
            evt_list.append(test_event)
        return evt_list if len(evt_list) > 1 else evt_list[0]

    def test_create_event(self):
        response = self.client.post(
            '/api/fbapp/events',
            headers={"Content-Type": "application/json",
                     "X_API_KEY": self.app.config['API_KEY']},
            data=json.dumps(self.event_json))

        self.assertEqual(response.status_code, 201)

    def test_get_event_list(self):
        nb_insert = 500
        t0 = timer()
        events_list = self.__make_test_event(nb_insert)
        for event in events_list:
            db.session.add(event)
        db.session.commit()
        insert_time = timer() - t0
        print('insert_time:', insert_time)
        print('key:', self.app.config['API_KEY'])
        response = self.client.get('/api/fbapp/events', headers={"X_API_KEY": self.app.config['API_KEY']})
        data = response.get_json()

        self.assert200(response)
        self.assertEqual(type(data), list)
        self.assertEqual(nb_insert, len(data))

    def test_get_event_by_public_id(self):
        event = self.__make_test_event(1)
        db.session.add(event)
        db.session.commit()
        response = self.client.get('/api/fbapp/event/' + event.public_id, headers={"X_API_KEY": self.app.config['API_KEY']})
        data = response.get_json()

        self.assert200(response)
        self.assertEqual(data['public_id'], event.public_id)
        self.assertEqual(data['psid'], event.psid)

    def test_delete_all_events(self):
        events_list = self.__make_test_event(5)
        for event in events_list:
            db.session.add(event)
        db.session.commit()
        response = self.client.delete('/api/fbapp/events', headers={"X_API_KEY": self.app.config['API_KEY']})
        self.assert200(response)

    def test_delete_by_public_id(self):
        event = Event(
            public_id='test1_public_id',
            psid='test1',
            recipient_id='test1',
            timestamp=0
        )
        db.session.add(event)
        db.session.commit()
        response = self.client.delete('/api/fbapp/event/1', headers={"X_API_KEY": self.app.config['API_KEY']})
        self.assert200(response)

    def test_fb_verif(self):
        challenge = 'test_challenge'
        token = 'test_token'
        self.app.config['FB_VERIFY_TOKEN'] = token
        # cannot request the api directly due to the response type
        response = make_response(_fbapp_services.handle_fbverif(token, challenge))
        self.assert200(response)


if __name__ == '__main__':
    unittest.main()
