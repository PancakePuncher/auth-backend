from typing import Annotated
from fastapi import APIRouter, Header, Cookie, BackgroundTasks
from pydantic import BaseModel, EmailStr
from util.database import DatabaseActions
from util.email import EmailActions

user_router = APIRouter(prefix="/user")


class Email(BaseModel):
    email: EmailStr


class UserRegInfo(BaseModel):
    username: str
    password: str
    setupCode: str


@user_router.post("/register")
def validate_authentication(
    user_reg_info: UserRegInfo,
    x_forwarded_host: Annotated[str | None, Header()] = None,
    x_forwarded_uri: Annotated[str | None, Header()] = None,
    x_pp_auth_token: Annotated[str | None, Cookie()] = None,
):
    print(x_forwarded_host, x_forwarded_uri, x_pp_auth_token)
    print(user_reg_info)
    return {"test": "test"}


@user_router.post("/get_code")
async def get_reg_code(data: Email, background_tasks: BackgroundTasks):
    code = await DatabaseActions.get_code(email=data.email)
    background_tasks.add_task(EmailActions.send, data.email, code)
    return {"reg_code": code}
