from argon2 import PasswordHasher


class Security:
    ph = PasswordHasher()

    async def hash(password):
        hashed = Security.ph.hash(password)

        return hashed

    async def verify_against_hash(hashed_password, password):
        verified = Security.ph.verify(hashed_password, password)

        return verified
