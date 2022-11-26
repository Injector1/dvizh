from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField


class ArticleModel(Model):
    id = fields.CharField(max_length=255)
    team_name = fields.CharField(max_length=128)
    telegraph_articles_urls = ArrayField('str', null=True)
