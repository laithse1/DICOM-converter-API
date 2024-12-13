import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secure-secret-key"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60

def create_jwt_token(username: str):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    payload = {
        "sub": username,
        "exp": expiration,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
