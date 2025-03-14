"""
docustring
"""
import socket
import json
from ds_protocol import extract_json


class DirectMessage:
    """
    docustring
    """

    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None

    def setting(self, recipient, message, timestamp=0):
        """
        docstring
        """
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp

    def jsontoobject(self, json_msg):
        """
        docustring
        """

        # print('json_to_object', json_msg)
        if 'from' in json_msg:
            self.recipient = f"from::{json_msg['from']}"
        else:
            self.recipient = json_msg['recipient']
        if 'message' in json_msg:
            self.message = json_msg['message']
        elif 'entry' in json_msg:
            self.message = json_msg['entry']
        self.timestamp = json_msg['timestamp']


class DirectMessenger:
    """
    docustring
    """
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        if dsuserver is not None:
            self.dsuserver = dsuserver
        else:
            self.dsuserver = '127.0.0.1'
        self.username = username
        self.password = password
        self.port = 3001
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.dsuserver, self.port))
        self.sendfile = self.client.makefile('w')
        self.recievefile = self.client.makefile('r')
        self.set_token()

    def set_token(self):
        """
        docustring
        """
        init_msg = {'join': {'username': self.username,
                    'password': self.password, 'token': self.token}}
        init_msg = json.dumps(init_msg)
        self.sendfile.write(init_msg)
        self.sendfile.flush()
        self.response = self.recievefile.readline()
        self.response = extract_json(self.response)
        self.token = self.response.token
        # print(self.token)

    def get_response(self):
        """
        docustring
        """
        return self.response

    def send(self, message: str, recipient: str) -> bool:
        """
        docustring
        """
        # must return true if message successfully sent, false if send failed.
        dm = DirectMessage()
        dm.setting(recipient, message, 0)
        sender = {
            'token': self.token,
            'directmessage': {
                'entry': dm.message,
                'recipient': dm.recipient,
                'timestamp': dm.timestamp
            }
        }
        sender = json.dumps(sender)
        self.sendfile.write(sender)
        self.sendfile.flush()
        response = self.recievefile.readline()
        # print(response)
        # print(type(response))
        response = extract_json(response)
        if response.type == 'ok':
            return True
        else:
            return False

    def retrieve_new(self) -> list:
        """
        docustring
        """
        # must return a list of DirectMessage objects
        # containing all new messages
        request = {'token': self.token,
                   'directmessage': 'new'}
        request = json.dumps(request)
        self.sendfile.write(request)
        self.sendfile.flush()
        response = self.recievefile.readline()
        response = extract_json(response)
        # print(response.message)
        result = []
        # print(type(response.message), response.message)
        if not isinstance(response.message, list):
            return result
        for item in response.message:
            temp = DirectMessage()
            temp.jsontoobject(item)
            result.append(temp)
        return result

    def retrieve_all(self) -> list:
        """
        docustring
        """
        # must return a list of DirectMessage
        #  objects containing all messages
        request = {'token': self.token,
                   'directmessage': 'all'}
        request = json.dumps(request)
        self.sendfile.write(request)
        self.sendfile.flush()
        response = self.recievefile.readline()
        response = extract_json(response)
        # print(response.message)
        result = []
        if not isinstance(response.message, list):
            return result
        for item in response.message:
            temp = DirectMessage()
            print(temp)
            temp.jsontoobject(item)
            result.append(temp)
        # print(result[0].message)
        # print(result[1].message)
        return result


def test():
    """
    docustring
    """
    my_messenger = DirectMessenger('127.0.0.1', 'Kiara', '56789')
    sid_messenger = DirectMessenger('127.0.0.1', 'Sid', '89990')
    my_messenger.send('How is everyone?', 'Sid')
    print('---- new ----')
    sid_messenger.retrieve_new()
    print('---- all')
    sid_messenger.retrieve_all()


if __name__ == '__main__':
    test()
