# Hello!

This is a backend API for an Authentication portal I am building for my own personal homelab.
You can find the frontend portion of this code at: [My Authentication Frontend](https://github.com/PancakePuncher/auth-frontend)

Uses [UV](https://docs.astral.sh/uv/) as it's project manager.

This is primary built on:<br>
[FastAPI](https://fastapi.tiangolo.com/)<br>
[Piccolo ORM](https://piccolo-orm.com/)<br>

Other Security related things:<br>
Password hashing is done with [Argon2-cffi](https://github.com/hynek/argon2-cffi)<br>
Authentication/Authorization Tokens are handled by [PASETO - PySETO](https://github.com/dajiaji/pyseto)<br>
