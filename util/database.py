import datetime
from util.random import Generate
from database.models import ActiveRegCodes, Users


class DatabaseActions:
    async def get_code(email) -> int:
        selected = await ActiveRegCodes.select(ActiveRegCodes.reg_code).where(
            ActiveRegCodes.reg_email == str(email)
        )
        return selected[0]["reg_code"]

    async def check_code(email, code) -> bool:
        now = datetime.datetime.now(datetime.timezone.utc)
        try:
            selected = await ActiveRegCodes.select().where(
                (ActiveRegCodes.reg_email == str(email))
                & (ActiveRegCodes.reg_code == int(code))
            )
            delta = now - selected[0]["created_on"]
            if delta.days * 24 * 60 + delta.seconds / 60 >= 10:
                await ActiveRegCodes.update(
                    {
                        ActiveRegCodes.reg_code: Generate.ots(6),
                        ActiveRegCodes.created_on: datetime.datetime.now(
                            datetime.timezone.utc
                        ),
                    }
                ).where(
                    (ActiveRegCodes.reg_email == str(email))
                    & (ActiveRegCodes.reg_code == int(code))
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
