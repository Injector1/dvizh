from typing import List
from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel

from app.features.base import BaseRepository
from .schemas import *
from .models import TelegrafModel


class TelegrafRepository(BaseRepository):
    def __init__(self, model: TelegrafModel):
        self.model = model
        self.model_pydantic = pydantic_model_creator(TelegrafModel)
        self.model_pydantic_no_ids = pydantic_model_creator(TelegrafModel, exclude_readonly=True)

    async def get_by_team_name(self, team_name: str) -> List[PydanticModel]:
        return await self.model_pydantic_no_ids.from_queryset(TelegrafModel.filter(team_name=team_name))

    async def get_by_id(self, id: str) -> PydanticModel:
        return await self.model_pydantic.from_queryset_single(TelegrafModel.get(id=id))

    async def get_all(self) -> List[PydanticModel]:
        return await self.model_pydantic.from_queryset(TelegrafModel.all())

    async def create(self, article: TelegrafCreateOrUpdateScheme) -> PydanticModel:
        telegraf_article = await self.model.create(
            title=article.title,
            telegraf_url=article.url,
            team_name=article.team_name
        )
        print(telegraf_article)
        return await self.model_pydantic.from_tortoise_orm(telegraf_article)

    async def put(self, article: TelegrafCreateOrUpdateScheme) -> PydanticModel:
        await TelegrafModel.filter(url=article.url).update(**article.dict())
        return await self.model_pydantic_no_ids.from_queryset_single(TelegrafModel.get(url=article.url))
