"""
# This module implements OAuth authentication using Google with FastAPI and Authlib.
# It provides login and authentication endpoints.
# """

import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import models
from database import get_db

# Replace with your Auth0 values
AUTH0_DOMAIN = "dev-3vov0ik1g70405bg.us.auth0.com"
API_IDENTIFIER = "https://dev-3vov0ik1g70405bg.us.auth0.com/api/v2/"
ALGORITHMS = ["RS256"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_jwt(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, os.environ.get('AUTH0_PUBLIC_KEY'), algorithms=ALGORITHMS)
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Optionally, fetch user info from the database
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise credentials_exception

    return user




