from fastapi import APIRouter
from app.services.auth_service import signup, login, forgot_password, reset_password

router = APIRouter()


@router.post("/signup")
def signup_api(data: dict):
    return signup(
        data["email"],
        data["password"],
        data["organization"]
    )


@router.post("/login")
def login_api(data: dict):
    return login(
        data["email"],
        data["password"]
    )
    
@router.post("/forgot-password")
def forgot_api(data: dict):
    return forgot_password(data["email"])

@router.post("/reset-password")
def reset_api(data: dict):
    return reset_password(data["token"], data["new_password"])