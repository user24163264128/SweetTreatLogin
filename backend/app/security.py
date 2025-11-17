# app/security.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.jwt_creator import decode_token, is_access
from app.db import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
repo = UserRepository()


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Validates JWT access token and returns user data.
    """

    payload = decode_token(token)
    if not payload or not is_access(payload):
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    user_id = int(payload["sub"])

    # search in users and admins
    user = repo.db_user.find_by({"id": user_id})
    admin = repo.db_admin.find_by({"id": user_id})

    real_user = user[0] if user else (admin[0] if admin else None)

    if not real_user:
        raise HTTPException(status_code=404, detail="User not found")

    return real_user


def require_role(role: str):
    """
    Role enforcement decorator.
    """
    def checker(user=Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient privileges")
        return user
    return checker
