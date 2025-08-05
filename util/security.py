import pyseto
import time
import json
from config import enviroment_settings
from pyseto import Key
from argon2 import PasswordHasher


class Security:
    token_key = Key.new(
        version=4, purpose="local", key=bytes(enviroment_settings.TOKEN_SECRET, "utf-8")
    )
    ph = PasswordHasher()

    async def hash(password):
        hashed = Security.ph.hash(password)

        return hashed

    async def verify_against_hash(hashed_password, password):
        verified = Security.ph.verify(hashed_password, password)

        return verified

    async def encode_token():
        dict_payload = {
            "issued_on": time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(time.time())),
            "expired_at": time.strftime(
                "%a, %d-%b-%Y %T GMT", time.gmtime(time.time() + 2)
            ),
        }
        return pyseto.encode(
            Security.token_key, payload=bytes(str(dict_payload), "utf-8")
        ).decode()

    async def decode_token(token):
        return pyseto.decode(Security.token_key, token).payload.decode()
