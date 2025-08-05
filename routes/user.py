import time
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from util.database import DatabaseActions
from util.email import EmailActions
from util.security import Security
from config import enviroment_settings

user_router = APIRouter(prefix="/user")


class Email(BaseModel):
    email: EmailStr


class UserLoginInfo(BaseModel):
    email: EmailStr
    password: str


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
async def user_register(
    user_reg_info: UserRegInfo,
):
    is_code_valid = await DatabaseActions.check_code(
        email=user_reg_info.email, code=user_reg_info.setupCode
    )
    if is_code_valid is True:
        user_reg_info.password = await Security.hash(user_reg_info.password)
        await DatabaseActions.create_user(user_reg_info)
        await DatabaseActions.delete_code(
            email=user_reg_info.email, code=user_reg_info.setupCode
        )
        return 200
    else:
        raise HTTPException(status_code=400)
    return 200


@user_router.post("/login")
async def user_login(user_login_info: UserLoginInfo):
    stored_user = await DatabaseActions.get_user_by_email(user_login_info.email)
    if stored_user is not False:
        verified = await Security.verify_against_hash(
            stored_user["password"], user_login_info.password
        )
    else:
        raise HTTPException(status_code=400)

    if verified is False:
        raise HTTPException(status_code=400)

    response = JSONResponse(content={"Status": "Successful"})
    response.set_cookie(
        key="x_pp_auth_token",
        value=str(await Security.encode_token()),
        httponly=True,
        domain=f".{enviroment_settings.YOUR_DOMAIN}",
        secure=True,
        samesite="lax",
        expires=time.strftime(
            "%a, %d-%b-%Y %T GMT",
            time.gmtime(time.time() + 2),  ## VALID FOR 1 DAY (24 HOURS)
        ),
    )

    return response
