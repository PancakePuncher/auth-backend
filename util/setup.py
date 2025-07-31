import tomllib
from pony import orm
from config import enviroment_settings


class Setup:
    def initialization(database):
        with open("./util/status.toml", "rb") as f:
            data = tomllib.load(f)
        if data["status"]["stage"] == "setup":
            with orm.db_session:
                database.UserSetup(for_email=enviroment_settings.ADMIN_EMAIL)
