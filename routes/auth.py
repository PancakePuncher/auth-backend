from typing import Annotated
from fastapi import APIRouter, Header, Cookie
from fastapi.responses import RedirectResponse
from util.security import Security

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/validate")
async def validate_authentication(
    x_forwarded_host: Annotated[str | None, Header()] = None,
    x_forwarded_uri: Annotated[str | None, Header()] = None,
    x_pp_auth_token: Annotated[str | None, Cookie()] = None,
):
    print(x_forwarded_host, x_forwarded_uri, x_pp_auth_token)
    if x_pp_auth_token:
        decoded = await Security.decode_token(x_pp_auth_token)
        print(decoded)
    return 200
