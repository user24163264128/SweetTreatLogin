# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from app.jwt_creator import create_access_token, create_refresh_token, decode_token, is_refresh
from app.hashing import verify_password, hash_password
from app.db import UserRepository
from app.models_schema import UserSchema, AdminSchema
from datetime import timedelta
from app.security import get_current_user, require_role

app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_repo = UserRepository()


# ----------------------------------------------------------------------
#  REGISTER (User or Admin)
# ----------------------------------------------------------------------
@app.post("/auth/register")
def register_user(data: dict):
    """
    Register user or admin based on 'role'.
    """
    required_fields = ["id", "username", "email", "password"]

    if not all(k in data for k in required_fields):
        raise HTTPException(status_code=400, detail="Missing registration fields")

    hashed_pw = hash_password(data["password"])

    # Construct base fields
    base = {
        "id": data["id"],
        "username": data["username"],
        "email": data["email"],
        "password_hash": hashed_pw,
    }

    if data.get("role") == "admin":
        # Create admin
        admin_data = AdminSchema(**base)
        user_repo.add_admin(admin_data.model_dump())
        return {"msg": "Admin registered"}

    # Otherwise user
    user_data = UserSchema(**base)
    user_repo.add_user(user_data.model_dump())
    return {"msg": "User registered"}


# ----------------------------------------------------------------------
#  LOGIN
# ----------------------------------------------------------------------
@app.post("/auth/login")
def login(response: Response, form: OAuth2PasswordRequestForm = Depends()):
    """
    Login using OAuth2 form:
    username = email
    password = password
    """

    # find users or admins
    users = user_repo.db_user.find_by({"email": form.username})
    admins = user_repo.db_admin.find_by({"email": form.username})

    user = users[0] if users else (admins[0] if admins else None)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(form.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    user_id = user["id"]
    role = user["role"]

    # Create tokens
    access = create_access_token({"sub": str(user_id), "role": role})
    refresh = create_refresh_token({"sub": str(user_id), "role": role})

    # Set refresh token in HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=False,     # set True in production
        samesite="lax",
        max_age=60 * 60 * 24 * 30
    )

    return {
        "message": "Login successful",
        "access_token": access,
        "token_type": "bearer",
        "redirect": "/dashboard/admin" if role == "admin" else "/dashboard/user"
    }


# ----------------------------------------------------------------------
#  REFRESH TOKEN USING HTTPONLY COOKIE
# ----------------------------------------------------------------------
@app.post("/auth/refresh")
def refresh_token(refresh_token: str | None = Cookie(default=None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    decoded = decode_token(refresh_token)

    if not decoded or not is_refresh(decoded):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # create new access token
    new_access = create_access_token({
        "sub": decoded["sub"],
        "role": decoded["role"]
    })

    return {"access_token": new_access, "token_type": "bearer"}


@app.get("/auth/me")
def auth_me(user = Depends(get_current_user)):
    """
    Returns the logged-in user's profile based on access token.
    """
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"]
    }

# ----------------------------------------------------------------------
# LOGOUT — clears the refresh token cookie
# ----------------------------------------------------------------------
@app.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}

# ----------------------------------------------------------------------
#  DASHBOARD ENDPOINTS (protected)
# ----------------------------------------------------------------------
@app.get("/dashboard/user")
def user_dashboard(user = Depends(require_role("user"))):
    return {"message": f"Welcome USER {user['username']}"}

@app.get("/dashboard/admin")
def admin_dashboard(admin = Depends(require_role("admin"))):
    return {"message": f"Welcome ADMIN {admin['username']}"}
