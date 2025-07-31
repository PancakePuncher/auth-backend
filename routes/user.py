from typing import Annotated
from fastapi import APIRouter, Header, Cookie
from pydantic import BaseModel

user_router = APIRouter(prefix="/user")


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
