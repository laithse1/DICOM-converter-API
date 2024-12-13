from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import jwt
import logging

SECRET_KEY = "your-secure-secret-key"
API_KEYS = {"client1": "client1-api-key", "client2": "client2-api-key"}  # Replace with your API keys

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def authentication_middleware(request: Request, call_next):
    try:
        # Check for JWT or API Key in the request headers
        auth_header = request.headers.get("Authorization")
        api_key = request.headers.get("x-api-key")
        if api_key and api_key in API_KEYS.values():
            logging.info(f"Authenticated with API Key: {api_key}")
        elif auth_header and "Bearer" in auth_header:
            token = auth_header.split(" ")[1]
            verify_jwt_token(token)
            logging.info(f"Authenticated with JWT: {token}")
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")
        return await call_next(request)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
