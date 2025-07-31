import uvicorn
from tomlkit import parse, dumps
from piccolo.table import create_db_tables
from contextlib import asynccontextmanager
from routes.v1 import v1_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import enviroment_settings
from database.models import ActiveRegCodes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # CREATES POSTGRESQL DATABASES IF THEY DONT EXIST
    await create_db_tables(ActiveRegCodes, if_not_exists=True)

    # OPENS APPLICATION STATUS TOML
    with open("status.toml", "rb") as f:
        status_file = parse(f.read())

    # IF THE STATUS IS SETUP WE ARE GOING TO DO SOME STUFF
    if status_file["status"]["stage"] == "setup":
        try:
            await ActiveRegCodes.insert(
                ActiveRegCodes(reg_email=enviroment_settings.ADMIN_EMAIL)
            )
        except Exception:
            pass

    status_file["status"]["stage"] = "deployed"
    with open("status.toml", "w") as f:
        f.write(dumps(status_file))
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(v1_router)

origins = ["http://vue.pancakepuncher.com", "https://vue.pancakepuncher.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5050, log_level=0, reload=True)
