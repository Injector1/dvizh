from tortoise.models import Model
from tortoise import fields


class UserModel(Model):
    chat_id = fields.CharField(max_length=64, unique=True)
    username = fields.CharField(max_length=64, unique=True)
    subscribed_team = fields.CharField(max_length=64)
