import asyncio
from typing import List
import json

from app.features.base import BaseRepository
from app.features.telegraf.schemas import *
from app.features.telegraf.models import TelegrafModel


class JsonRepository(BaseRepository):
    def __init__(self, model: TelegrafModel):
        self.model = model
        self.file = './database/data.json'

    def get_by_id(self, id: str) -> TelegrafScheme:
        for data in json.load(open(self.file, encoding='utf-8'))['articles']:
            telegraf_obj = TelegrafScheme(**data)
            if telegraf_obj.id == id:
                return telegraf_obj

    def find_all(self, **kwargs) -> List[TelegrafScheme]:
        key, value = list(kwargs.items())[0]
        result = []
        for data in json.load(open(self.file, encoding='utf-8'))['articles']:
            if key in data.keys():
                if data[key] == value:
                    result.append(TelegrafScheme(**data))
        return result

    def get_all(self) -> List[TelegrafScheme]:
        result = []
        for data in json.load(open(self.file, encoding='utf-8'))['articles']:
            result.append(TelegrafScheme(**data))
        return result

    async def create(self, article: TelegrafCreateOrUpdateScheme) -> TelegrafScheme:
        data = json.load(open(self.file, encoding='utf-8'))
        await asyncio.sleep(0.1)
        similar = self.find_all(title=article.title)
        if len(similar) == 0:
            telegraf_obj = TelegrafScheme(id=len(data['articles']) + 1, **article.dict())
            data['articles'].append(telegraf_obj.dict())
            with open(self.file, "w", encoding='utf-8') as outfile:
                outfile.write(json.dumps(data, indent=4))
            return telegraf_obj
        return TelegrafScheme(id=similar[0].id, **article.dict())

    def put(self, article: TelegrafCreateOrUpdateScheme) -> TelegrafScheme:
        input_data = json.load(open(self.file, encoding='utf-8'))
        for i in range(len(input_data['articles'])):
            data = input_data['articles'][i]
            t = TelegrafScheme(**data)
            if t.url == article.url:
                telegraf_obj = TelegrafScheme(id=t.id, **article.dict())
                input_data['articles'][i] = telegraf_obj.dict()

                with open(self.file, "w", encoding='utf-8') as outfile:
                    outfile.write(json.dumps(input_data, indent=4))
                return telegraf_obj
