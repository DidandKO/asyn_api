import os

from starlette.config import Config

config = Config(".env_dev")

os.environ['ASYN_DB'] = "postgresql://root:root@localhost:32700/asyn"

DATABASE_URL = config("ASYN_DB", cast=str, default='')

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
SECRET_KEY = config("ASYN_SECRET_KEY", cast=str, default="1"*32)
