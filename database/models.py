import datetime
import uuid
from util.random import Generate
from piccolo.table import Table
from piccolo.columns import Integer, Timestamptz, Varchar, UUID


class ActiveRegCodes(Table):
    reg_email = Varchar(unique=True)
    reg_code = Integer(unique=True, default=Generate.ots(6))
    created_on = Timestamptz(default=datetime.datetime.now(datetime.timezone.utc))


class Users(Table):
    user_uuid = UUID(default=uuid.uuid4())
    display_name = Varchar(length=18)
    email = Varchar(unique=True)
    password = Varchar()
    created_on = Timestamptz(default=datetime.datetime.now(datetime.timezone.utc))
