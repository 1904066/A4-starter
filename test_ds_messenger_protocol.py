"""
docustring
"""
from collections import namedtuple
from ds_protocol import extract_json
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def test_extractjson():
    """
    docustring
    """
    response1 = (
        '{"response": {"type": "ok", '
        '"message": "Direct message sent"}}'
    )

    target1 = extract_json(response1)
    answer1 = DataTuple('ok', 'Direct message sent', '')
    assert target1 == answer1
    print('test 1 passed!')


def test_extractjson2():
    """
    docustring
    """
    response2 = (
        '{"response": {"type": "ok", "messages": ['
        '{"message": "Are you there?!", "from": "markb", '
        '"timestamp": "1603167689.3928561"}, '
        '{"message": "Bro? what happened?", "from":'
        ' "thebeemoviescript", '
        '"timestamp": "1603167689.3928561"}]}}'
    )

    target2 = extract_json(response2)
    messages = [
        {"message": "Are you there?!", "from":
            "markb", "timestamp": "1603167689.3928561"},
        {"message": "Bro? what happened?",
            "from": "thebeemoviescript", "timestamp":
         "1603167689.3928561"}
        ]
    answer2 = DataTuple('ok', messages, '')
    assert target2 == answer2
    print('test 2 passed!')


def test_extractjson3():
    """
    docustring
    """
    response3 = '{"response": {"type": "ok", "messages": '\
        '[{"message": "Are you there?!", '\
        '"from": "markb", "timestamp":"1603167689.3928561"},'\
        '{"message": ''"Yeah I just went to grab some water!'\
        'Jesus!", "recipient": "markb", ''"timestamp": '\
        '"1603167699.3928561"}, {"message":"Bzzzzz",'\
        '"from": ''"thebeemoviescript",'\
        '"timestamp": "1603167689.3928561"}]}}'
    target3 = extract_json(response3)
    messages = [
        {"message": "Are you there?!", "from": "markb",
            "timestamp": "1603167689.3928561"},
        {"message":
            "Yeah I just went to "
            "grab some water!Jesus!", "recipient":
            "markb",
            "timestamp": "1603167699.3928561"},
        {"message": "Bzzzzz", "from":
            "thebeemoviescript", "timestamp":
            "1603167689.3928561"}
        ]
    answer3 = DataTuple('ok', messages, '')
    # print(answer3)
    # print(target3)
    assert target3 == answer3
    print('test 3 passed!')


test_extractjson()
test_extractjson2()
test_extractjson3()
print('All tests passed!')
