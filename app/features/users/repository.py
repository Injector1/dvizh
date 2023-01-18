import asyncio
from typing import List
import json

from app.features.base import BaseRepository
from app.features.users.schemas import UserScheme
from app.features.users.models import UserModel


class UserRepository(BaseRepository):
    def __init__(self, model: UserModel):
        self.model = model
        self.file = './database/data.json'

    def get_by_id(self, id: str) -> UserScheme:
        for data in json.load(open(self.file, encoding='utf-8'))['users']:
            user_obj = UserScheme(**data)
            if user_obj.chat_id == id:
                return user_obj

    def find_all(self, **kwargs) -> List[UserScheme]:
        key, value = list(kwargs.items())[0]
        result = []
        for data in json.load(open(self.file, encoding='utf-8'))['users']:
            user_obj = UserScheme(**data)
            if key in data.keys():
                if data[key] == value:
                    result.append(user_obj)
        return result

    def get_all(self) -> List[UserScheme]:
        result = []
        for data in json.load(open(self.file, encoding='utf-8'))['users']:
            result.append(UserScheme(**data))
        return result

    def create(self, user: UserScheme) -> UserScheme:
        data = json.load(open(self.file, encoding='utf-8'))
        if len(self.find_all(chat_id=user.chat_id)) == 0:
            data['users'].append(user.dict())
            with open(self.file, "w", encoding='utf-8') as outfile:
                outfile.write(json.dumps(data, indent=4))
            return user

    def put(self, user: UserScheme) -> UserScheme:
        data = json.load(open(self.file, encoding='utf-8'))
        if len(self.find_all(chat_id=user.chat_id)) == 1:
            for d in data['users']:
                if d['chat_id'] == user.chat_id:
                    d['username'] = user.username
                    d['subscribed_team'] = user.subscribed_team
                    d['notify'] = user.notify
                    break
            with open(self.file, "w", encoding='utf-8') as outfile:
                outfile.write(json.dumps(data, indent=4))
            return user
