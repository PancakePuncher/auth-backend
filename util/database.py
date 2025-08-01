
from database.models import ActiveRegCodes


class DatabaseActions:
    async def get_code(email) -> int:
        selected = await ActiveRegCodes.select(ActiveRegCodes.reg_code).where(
            ActiveRegCodes.reg_email == str(email)
        )
        return selected[0]["reg_code"]

        