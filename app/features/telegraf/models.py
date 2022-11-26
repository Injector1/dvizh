from tortoise.models import Model
from tortoise import fields


class ArticleModel(Model):
    id = fields.CharField(max_length=255)
    title = fields.CharField(max_length=128)
    url = fields.CharField(max_length=1000000)

