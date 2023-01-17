from dependency_injector import containers, providers

from .repository import TelegrafRepository
from .json_repo import JsonRepository
from .models import TelegrafModel
from .service import TelegrafService


class TelegrafContainer(containers.DeclarativeContainer):
    telegraf = providers.Dependency()
    account_name = providers.Dependency()

    telegraf_model = providers.Factory(TelegrafModel)
    telegraf_repository = providers.Singleton(
        JsonRepository,
        model=telegraf_model,
    )
    telegraf_service = providers.Singleton(
        TelegrafService,
        telegraf=telegraf,
        telegraf_repository=telegraf_repository,
        account_name=account_name
    )

