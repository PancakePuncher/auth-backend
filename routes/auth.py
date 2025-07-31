from typing import Annotated
from fastapi import APIRouter, Header, Cookie
from fastapi.responses import RedirectResponse

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/validate")
def validate_authentication(
    x_forwarded_host: Annotated[str | None, Header()] = None,
    x_forwarded_uri: Annotated[str | None, Header()] = None,
    x_pp_auth_token: Annotated[str | None, Cookie()] = None,
):
    print(x_forwarded_host, x_forwarded_uri, x_pp_auth_token)
    return RedirectResponse(
        "https://vue.pancakepuncher.com/",
        status_code=307,
        headers=None,
    )
