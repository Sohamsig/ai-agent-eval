import json


def parse_json(value):
    return json.loads(value)


def get_user_name(data):
    return data["user"]["name"]