from argon2 import PasswordHasher


class Security:
    async def hash(password):
        ph = PasswordHasher()
        hashed = ph.hash(password)

        return hashed
