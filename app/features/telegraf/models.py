from tortoise.models import Model
from tortoise import fields


class TelegrafModel(Model):
    title = fields.CharField(max_length=255, unique=True)
    telegraf_url = fields.CharField(max_length=255)
    team_name = fields.CharField(max_length=64)
