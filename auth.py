from datetime import datetime, timedelta
from jose import jwt

SECRET = "secret"

def create_token(data: dict):
    return jwt.encode(data, SECRET, algorithm="HS256")