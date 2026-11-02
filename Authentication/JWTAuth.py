import jwt
import os
from datetime import datetime,timedelta, timezone
from fastapi import Cookie,HTTPException



secret_key = os.getenv("JWT_SECRET")
Algorithm = os.getenv("ALGORITHM")
exp_minutes = int(os.getenv("TOKEN_EXPIRATION"))  

def create_jwt_token(userid):
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)
    payload = {
        "userid": userid,
        "iat": datetime.now(timezone.utc),
        "exp": exp_time.timestamp()
    }

    token = jwt.encode(payload, secret_key, algorithm=Algorithm)
    print("Generated JWT Token:", token)
    return token

def decode_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, secret_key, algorithms=[Algorithm])
        return decoded_payload["userid"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    


def check_the_user(token: str = Cookie(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    try:
        decoded_user_id = decode_jwt_token(token)
        return int(decoded_user_id)
    except HTTPException as e:
        raise HTTPException(status_code=401, detail=f" {e.detail}")

