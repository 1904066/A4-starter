"""
docustring
"""
# ds_protocol.py

# PRIYANKAA NIGAM
# PNNIGAM@UCI.EDU
# 50285154


import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on
    a json string and convert it to
    a DataTuple object

    TODO: replace the pseudo placeholder
    keys with actual DSP protocol keys
    '''
    message = None
    response_type = None
    token = None
    try:
        json_obj = json.loads(json_msg)
        # foo = json_obj['foo']
        # baz = json_obj['bar']['baz']
        response_type = json_obj['response']['type']
        if 'messages' in json_obj['response']:
            message = json_obj['response']['messages']
        if 'message' in json_obj['response']:
            message = json_obj['response']['message']
        if 'token' in json_obj['response']:
            token = json_obj['response']['token']
        else:
            token = ''
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    return DataTuple(response_type, message, token)


def test(js):
    """
    docustring
    """
    data = extract_json(js)
    print(data)
    print(data.type)
    print(data.message)
    print(data.token)
    # temp = '{"response": {"type": "ok",
    # "message": "", "token":"12345678-1234-
    # 1234-1234-123456789abc"}}'
    # test(temp)
