from typing import List

from app.features.base import BaseRepository
from .schemas import *


class TelegrafRepository(BaseRepository):
    def get_by_id(self, id: str) -> TelegrafScheme:
        pass

    def get_all(self) -> List[TelegrafScheme]:
        pass

    def create(self, article: TelegrafCreateOrUpdateScheme) -> TelegrafScheme:
        pass

    def put(self, article: TelegrafCreateOrUpdateScheme) -> TelegrafScheme:
        pass
