from os import getenv

# payok.io settings
SHOP = 9340
CURRENCY = "RUB"
SECRET = getenv("SECRET")

# auth settings
SECRET_KEY = getenv("SECRET_KEY")

# telegram token
TG_TOKEN = getenv("TG_TOKEN")

# IGDB API credentials
CLIENT_ID_IGDB = getenv("CLIENT_ID")
AUTH_IGDB = getenv("AUTH_IGDB")

# mongodb connection string
MONGODB_CONNECT = getenv("MONGODB_CONNECT")
