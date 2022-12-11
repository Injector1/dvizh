import json


FILE = './database/data.json'


def get_from_database() -> dict:
    return json.load(open(FILE, encoding='utf-8'))['users']


def add_to_database(user_id: str, team: str) -> None:
    data = json.load(open(FILE, encoding='utf-8'))
    data['users'][user_id] = team
    with open(FILE, "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(data, indent=4))