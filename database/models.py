import datetime
from util.random import Generate
from piccolo.table import Table
from piccolo.columns import Integer, Email, Timestamptz


class ActiveRegCodes(Table):
    reg_email = Email(unique=True)
    reg_code = Integer(unique=True, default=Generate.ots(6))
    created_on = Timestamptz(default=datetime.datetime.now(datetime.timezone.utc))
