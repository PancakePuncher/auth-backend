import datetime
from typing import Union
from util.random import Generate
from database.models import ActiveRegCodes, Users


class DatabaseActions:
    now = datetime.datetime.now(datetime.timezone.utc)

    async def regen_code(email, code, new_code=Generate.ots(6)) -> None:
        print(email, code, new_code)
        await ActiveRegCodes.update(
            {
                ActiveRegCodes.reg_code: new_code,
                ActiveRegCodes.created_on: datetime.datetime.now(datetime.timezone.utc),
            }
        ).where(
            (ActiveRegCodes.reg_email == str(email))
            & (ActiveRegCodes.reg_code == int(code))
        )

        return

    async def get_code(email) -> int:
        selected = await ActiveRegCodes.select().where(
            ActiveRegCodes.reg_email == str(email)
        )
        delta = DatabaseActions.now - selected[0]["created_on"]
        if delta.days * 24 * 60 + delta.seconds / 60 >= 10:
            code = Generate.ots(6)
            await DatabaseActions.regen_code(
                email=email, code=selected[0]["reg_code"], new_code=code
            )
            return code
        return selected[0]["reg_code"]

    async def check_code(email, code) -> bool:
        try:
            selected = await ActiveRegCodes.select().where(
                (ActiveRegCodes.reg_email == str(email))
                & (ActiveRegCodes.reg_code == int(code))
            )
            delta = DatabaseActions.now - selected[0]["created_on"]
            if delta.days * 24 * 60 + delta.seconds / 60 >= 10:
                await DatabaseActions.regen_code(
                    ActiveRegCodes.reg_email, ActiveRegCodes.reg_code
                )
                return False
        except Exception:
            return False
        return True

    async def delete_code(email, code) -> None:
        await ActiveRegCodes.delete().where(
            (ActiveRegCodes.reg_email == str(email))
            & (ActiveRegCodes.reg_code == int(code))
        )
        return

    async def create_user(user) -> bool:
        try:
            await Users.insert(
                Users(
                    display_name=user.display_name,
                    email=user.email,
                    password=user.password,
                )
            )
            return True
        except Exception:
            return False

    async def get_user_by_email(email) -> Union[object, False]:
        try:
            stored_user = await Users.select().where(Users.email == email)
        except Exception:
            return False
        return stored_user[0]
