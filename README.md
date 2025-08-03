# Hello!

This is a backend API for an Authentication portal I am building for my own personal homelab.
You can find the frontend portion of this code at: [My Authentication Frontend](https://github.com/PancakePuncher/auth-frontend)

Uses [UV](https://docs.astral.sh/uv/) as it's project manager.

This is primary built on:

[FastAPI](https://fastapi.tiangolo.com/)
[Piccolo ORM](https://piccolo-orm.com/)

Other Security related things:

Password hashing is done with [Argon2-cffi](https://github.com/hynek/argon2-cffi)
Authentication/Authorization Tokens are handled by [PASETO - PySETO](https://github.com/dajiaji/pyseto)