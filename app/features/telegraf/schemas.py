from pydantic import BaseModel


class ArticleScheme(BaseModel):
    id: str
    title: str
    content: str
    team_name: str


class ArticleCreateOrUpdateScheme(BaseModel):
    title: str
    content: str
    team_name: str


class TelegrafScheme(BaseModel):
    id: str
    title: str
    url: str
    team_name: str


class TelegrafCreateOrUpdateScheme(BaseModel):
    title: str
    url: str
    team_name: str
