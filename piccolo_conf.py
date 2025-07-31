from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine
from config import enviroment_settings

DB = PostgresEngine(
    config={
        "host": "localhost",
        "port": "5432",
        "database": enviroment_settings.POSTGRES_DATABASE,
        "user": enviroment_settings.POSTGRES_USER,
        "password": enviroment_settings.POSTGRES_USER_PASSWORD,
    }
)

APP_REGISTRY = AppRegistry(apps=[])
