from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
from util.database import DatabaseActions
from util.email import EmailActions

user_router = APIRouter(prefix="/user")


class Email(BaseModel):
    email: EmailStr


class UserRegInfo(BaseModel):
    display_name: str
    email: EmailStr
    password: str
    setupCode: str


@user_router.post("/get_code")
async def get_reg_code(data: Email, background_tasks: BackgroundTasks):
    code = await DatabaseActions.get_code(email=data.email)
    background_tasks.add_task(EmailActions.send, data.email, code)
    return 200


@user_router.post("/register")
async def validate_authentication(
    user_reg_info: UserRegInfo,
):
    is_code_valid = await DatabaseActions.check_code(
        email=user_reg_info.email, code=user_reg_info.setupCode
    )
    if is_code_valid is True:
        await DatabaseActions.create_user(user_reg_info)
        await DatabaseActions.delete_code(
            email=user_reg_info.email, code=user_reg_info.setupCode
        )
        return 200
    else:
        raise HTTPException(status_code=400)
    return 200
