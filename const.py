import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("HASH_ALGORITHM")
TOKEN_EXPIRE_TIME = 30