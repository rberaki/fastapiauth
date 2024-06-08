from decouple import config

DB_URL = config('DATABASE_URL')
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
TOKEN_EXPIRE_MINUTES = config('TOKEN_EXPIRE_MINUTES', cast=int)
ISSUER = config("ISSUER")
AUDIENCE = config("AUDIENCE")
