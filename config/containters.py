from dependency_injector import containers, providers

from .databaseORM import DatabaseORM
from service.testService import TestService
from dao.testDao import TestDao


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=["controller.testController"])

    config = providers.Configuration(yaml_files=["config.yml"])

    dbORM = providers.Singleton(DatabaseORM, db_url=config.db.url)
    
    test_dao = providers.Factory(
        TestDao,
        session_factory=dbORM.provided.session,
    )
    
    test_service = providers.Factory(
      TestService,
      test_dao=test_dao,
    )