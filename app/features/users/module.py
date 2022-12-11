from dependency_injector import containers, providers

from .repository import UserRepository
from .service import UserService
from .models import UserModel


class UserContainer(containers.DeclarativeContainer):
    user_model = providers.Factory(UserModel)

    user_repository = providers.Singleton(
        UserRepository,
        model=user_model
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )

