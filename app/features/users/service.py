from app.features.users.schemas import UserScheme
from app.features.telegraf.json_repo import JsonRepo


class UserService:
    def __init__(self, user_repository: JsonRepo):
        self.user_repository = user_repository

    async def create_user(self, user_to_create: UserScheme):
        '''
        Разобраться с юзер репо и чики пуки
        user = await self.user_repository.create(user_to_create)
        return user
        '''
        pass
