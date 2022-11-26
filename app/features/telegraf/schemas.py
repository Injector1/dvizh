from pydantic import BaseModel


class Article(BaseModel):
    id: str
    title: str
    content: str


class ArticleCreate(BaseModel):
    title: str
    content: str
