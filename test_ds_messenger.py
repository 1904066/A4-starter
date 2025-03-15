"""
docustring
"""

import time
from ds_messenger import DirectMessage, DirectMessenger


# def connect_to_server(name, password):
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(('127.0.0.1', 3001))
#     send = client.makefile('w')
#     receive = client.makefile('r')
#     init_msg = json.dumps({'join': {'username': name,
#     'password': password, 'token': ''}})
#     send.write(init_msg)
#     send.flush()
#     response = extract_json(receive.readline())
#     token = response.token
#     return client, send, receive, token
#     def test_send(send, receive, name, password):
#     init_msg = json.dumps({'join': {'username':
#     name, 'password': password, 'token': ''}})
#     send.write(init_msg)
#     send.flush()
#     response = extract_json(receive.readline())
#     answer = extract_json('{"response":
#     {"type": "ok", "message": f"Welcome back, {name}"}')
#     assert response.response_type == answer.response_type
#     assert response.message == answer.message
#     print('Test 1 passed!')
# k_client, k_send, k_recieve, k_token = connect_to_server('Kiara', '56789')
# #a_client, a_send, a_recieve, a_token = connect_to_server('Alia', '66666')

# test_send(k_send, k_recieve, 'Kiara', '56789')


def test_connect_success():
    """
    docustring
    """
    my_messenger = DirectMessenger('127.0.0.1', 'Kiara', '56789')
    response = my_messenger.get_response()
    assert response.type == 'ok'
    print('test 2 passed!')


def test_connect_fail():
    """
    docustring
    """
    my_messenger = DirectMessenger('127.0.0.1', 'Kiara', 'wrong password')
    response = my_messenger.get_response()
    assert response.type == 'error'
    print('test 1 passed!')


def test_send_fail():
    """
    docustring
    """
    my_messenger = DirectMessenger('127.0.0.1', 'Kiara', '56789')
    assert my_messenger.send('hello', 'Mario') is False
    print('test 3 passed!')


def test_send_success():
    """
    docustring
    """
    my_messenger = DirectMessenger('127.0.0.1', 'Kiara', '56789')
    sid_messenger = DirectMessenger('127.0.0.1', 'Sid', '1234')
    assert my_messenger.send('hello', 'Sid') is True
    print('test 4 passed!')


def test_retrieve_new():
    """
    docustring
    """
    my_messenger = DirectMessenger('127.0.0.1', 'Kiara', '56789')
    name = "new" + str(round(time.time()))
    user = DirectMessenger('127.0.0.1', name, '1234')
    my_messenger.send('hello', name)
    messages = user.retrieve_new()
    assert isinstance(messages, list)
    # print(messages)
    # assert len(messages) == 1
    assert isinstance(messages[0], DirectMessage)
    assert messages[0].recipient == 'from::Kiara'
    assert messages[0].message == 'hello'
    print('test 5 passed!')


def test_retrieve_all():
    """
    docustring
    """
    my_messenger = DirectMessenger('127.0.0.1', 'Kiara', '56789')
    name = "all" + str(round(time.time()))
    user = DirectMessenger('127.0.0.1', name, '1234')
    my_messenger.send('hello', name)
    my_messenger.send('hey', name)
    my_messenger.send('hi', name)
    messages = user.retrieve_new()
    messages = user.retrieve_all()
    assert isinstance(messages, list)
    assert isinstance(messages[0], DirectMessage)
    assert isinstance(messages[1], DirectMessage)
    assert isinstance(messages[2], DirectMessage)
    assert messages[0].recipient == 'from::Kiara'
    assert messages[0].message == 'hello'
    assert messages[1].recipient == 'from::Kiara'
    assert messages[1].message == 'hey'
    assert messages[2].recipient == 'from::Kiara'
    assert messages[2].message == 'hi'
    print('test 6 passed!')


# def unit_test():
#     """
#     docustring
#     """
#     test_connect_fail()
#     test_connect_success()
#     test_send_fail()
#     test_send_success()
#     test_retrieve_new()
#     test_retrieve_all()
#     print('all tests passed!')


# if __name__ == "__main__":
#     unit_test()
