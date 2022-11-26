from typing import List

from app.features.base import BaseRepository
from schemas import *


class ArticleRepository(BaseRepository):
    def get_by_id(self, id: str) -> Article:
        pass

    def get_all(self) -> List[Article]:
        pass

    def create(self, article: ArticleCreate) -> Article:
        pass

    def put(self, *args, **kwargs) -> Article:
        pass
