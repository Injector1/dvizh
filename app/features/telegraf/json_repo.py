from typing import List
import json

from app.features.base import BaseRepository
from app.features.telegraf.schemas import *
from app.features.telegraf.models import TelegrafModel


class JsonRepo(BaseRepository):
    def __init__(self, model: TelegrafModel):
        self.model = model
        self.file = 'data.json'

    def get_by_id(self, id: str) -> TelegrafScheme:
        for data in json.load(open(self.file, encoding='utf-8'))['articles']:
            telegraf_obj = TelegrafScheme.parse_obj(json.loads(data))
            if telegraf_obj.id == id:
                return telegraf_obj

    def get_all(self) -> List[TelegrafScheme]:
        data = json.load(open(self.file, encoding='utf-8'))

        result = []
        for i in data['articles']:
            result.append(TelegrafScheme.parse_obj(json.loads(i)))
        return result

    def create(self, article: TelegrafCreateOrUpdateScheme) -> TelegrafScheme:
        data = json.load(open(self.file, encoding='utf-8'))

        telegraf_obj = TelegrafScheme(id=len(data['articles']) + 1, **article.dict())
        data['articles'].append(telegraf_obj.json())
        with open(self.file, "w", encoding='utf-8') as outfile:
            outfile.write(json.dumps(data, indent=4))

        return telegraf_obj

    def put(self, article: TelegrafCreateOrUpdateScheme) -> TelegrafScheme:
        m = json.load(open(self.file, encoding='utf-8'))
        for i in range(len(m['articles'])):
            data = m['articles'][i]
            t = TelegrafScheme.parse_obj(json.loads(data))
            if t.url == article.url:
                telegraf_obj = TelegrafScheme(id=t.id, **article.dict())
                m['articles'][i] = telegraf_obj.json()

                with open(self.file, "w", encoding='utf-8') as outfile:
                    outfile.write(json.dumps(m, indent=4))
                return telegraf_obj
