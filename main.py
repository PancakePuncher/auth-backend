import uvicorn
from routes.v1 import v1_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import enviroment_settings

app = FastAPI()
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
