from pydantic import BaseModel


class UserScheme(BaseModel):
    chat_id: str
    username: str
    subscribed_team: str
    notify: str
