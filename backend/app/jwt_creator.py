# # # app/utils/jwt.py

# # from datetime import datetime, timedelta, timezone
# # from typing import Optional, Dict, Any
# # import jwt

# # class Settings():
# #     def __init__(self):
# #         self.JWT_SECRET="b4f1cfa7db1ef0e8cd2a6e639ac3c2e75f835c0b4e99b9df28a3d7f63fc9a821"
# #         self.JWT_REFRESH_SECRET="6f92ad3b84c7ea1ccfbbb38de4a1be97e5a70291f072b0bd448a4b8db339df52"
# #         self.JWT_ALGORITHM = 'HS256'
# #         self.ACCESS_TOKEN_EXPIRE_MINUTES=15
# #         self.REFRESH_TOKEN_EXPIRE_DAYS=30

# # settings = Settings()

# # def create_access_token(data: Dict[str, Any]) -> str:
# #     """
# #     Creates a short-lived JWT access token.
# #     data (dict) MUST include: {"sub": user_id, "role": user_role}
# #     """
# #     to_encode = data.copy()
# #     expire = datetime.now(timezone.utc) + timedelta(
# #         minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
# #     )
# #     to_encode.update({"exp": expire, "type": "access"})

# #     return jwt.encode(
# #         to_encode,
# #         settings.JWT_SECRET,
# #         algorithm=settings.JWT_ALGORITHM
# #     )


# # def create_refresh_token(data: Dict[str, Any]) -> str:
# #     """
# #     Creates a long-lived JWT refresh token.
# #     data (dict) MUST include: {"sub": user_id, "role": user_role}
# #     """
# #     to_encode = data.copy()
# #     expire = datetime.now(timezone.utc) + timedelta(
# #         days=settings.REFRESH_TOKEN_EXPIRE_DAYS
# #     )
# #     to_encode.update({"exp": expire, "type": "refresh"})

# #     return jwt.encode(
# #         to_encode,
# #         settings.JWT_SECRET,
# #         algorithm=settings.JWT_ALGORITHM
# #     )


# # def decode_token(token: str) -> Optional[Dict[str, Any]]:
# #     """
# #     Decodes & verifies a JWT token.
# #     Returns payload dict or None if invalid/expired.
# #     """
# #     try:
# #         payload = jwt.decode(
# #             token,
# #             settings.JWT_SECRET,
# #             algorithms=[settings.JWT_ALGORITHM],
# #         )
# #         return payload
# #     except jwt.ExpiredSignatureError:
# #         return None  # expired token
# #     except jwt.InvalidTokenError:
# #         return None  # malformed token


# def is_access(payload: Dict[str, Any]) -> bool:
#     return payload.get("type") == "access"


# def is_refresh(payload: Dict[str, Any]) -> bool:
#     return payload.get("type") == "refresh"
# app/jwt_creator.py

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt

class Settings:
    def __init__(self):
        self.JWT_SECRET = "b4f1cfa7db1ef0e8cd2a6e639ac3c2e75f835c0b4e99b9df28a3d7f63fc9a821"
        self.JWT_REFRESH_SECRET = "6f92ad3b84c7ea1ccfbbb38de4a1be97e5a70291f072b0bd448a4b8db339df52"
        self.JWT_ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 15
        self.REFRESH_TOKEN_EXPIRE_DAYS = 30

settings = Settings()


def create_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "type": "access"})

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def create_refresh_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire, "type": "refresh"})

    return jwt.encode(
        to_encode,
        settings.JWT_REFRESH_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        # try access token first
        try:
            return jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.InvalidTokenError:
            # try refresh token
            return jwt.decode(
                token,
                settings.JWT_REFRESH_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def is_access(payload): return payload.get("type") == "access"
def is_refresh(payload): return payload.get("type") == "refresh"
